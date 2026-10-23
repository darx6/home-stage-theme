"""Create the Linden sofa demo product, its fabrics and the fabric sample product on HomeStage.

Run from the repo root: python3 -I media/setup/linden.py
Safe to rerun: definitions that already exist are skipped, products are matched by handle.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from shop import gql, check, upload, wait_files_ready

ROOT = os.path.join(os.path.dirname(__file__), "..", "linden")
FABRICS = json.load(open(os.path.join(ROOT, "fabrics.json")))
NS = "homestage"
MATERIAL = {
    "cobalt-wool": ("Dense woven wool", "Vacuum weekly. Spot clean with a damp cloth; do not rub."),
    "moss-boucle": ("Wool houndstooth tweed", "Vacuum with a brush head. Spot clean with a damp cloth; do not rub."),
    "ochre-velvet": ("Cotton velour velvet", "Brush with the pile. Steam lightly to lift pressure marks."),
    "oatmeal-linen": ("Washed rough linen", "Vacuum weekly. Blot spills straight away; professional clean only."),
    "charcoal-herringbone": ("Wool-poly herringbone", "Vacuum weekly. Spot clean with mild soap and water."),
    "plum-corduroy": ("Ribbed cotton corduroy", "Brush along the ribs. Spot clean with a damp cloth."),
}
STAGES = ["Frame built and joined", "Springs and webbing fitted", "Upholstered in your fabric", "Finished and inspected"]


def define_types():
    print("Fabric content type")
    check(gql("""mutation CreateFabricType($definition: MetaobjectDefinitionCreateInput!) {
      metaobjectDefinitionCreate(definition: $definition) {
        metaobjectDefinition { id type } userErrors { field message code } }}""", {"definition": {
        "type": f"{NS}_fabric", "name": "Fabric", "displayNameKey": "name",
        "access": {"storefront": "PUBLIC_READ"},
        "fieldDefinitions": [
            {"key": "number", "name": "Number", "type": "single_line_text_field", "required": True},
            {"key": "name", "name": "Name", "type": "single_line_text_field", "required": True},
            {"key": "colour", "name": "Colour", "type": "color", "required": True},
            {"key": "swatch", "name": "Swatch image", "type": "file_reference",
             "validations": [{"name": "file_type_options", "value": json.dumps(["Image"])}]},
            {"key": "material", "name": "Material", "type": "single_line_text_field"},
            {"key": "care", "name": "Care", "type": "multi_line_text_field"},
        ]}})["metaobjectDefinitionCreate"], "metaobjectDefinitionCreate")
    type_id = gql("""query { metaobjectDefinitionByType(type: "homestage_fabric") { id } }""",
                  mutate=False)["metaobjectDefinitionByType"]["id"]

    print("Product fields")
    fields = [
        ("fabrics", "Fabrics", "list.metaobject_reference", [{"name": "metaobject_definition_id", "value": type_id}]),
        ("width", "Width", "dimension", []),
        ("depth", "Depth", "dimension", []),
        ("height", "Height", "dimension", []),
        ("lead_time_min_weeks", "Lead time from (weeks)", "number_integer", []),
        ("lead_time_max_weeks", "Lead time to (weeks)", "number_integer", []),
        ("making_stages", "Making stages", "list.single_line_text_field", []),
        ("sample_product", "Sample product", "product_reference", []),
    ]
    for key, name, typ, validations in fields:
        check(gql("""mutation CreateFieldDef($definition: MetafieldDefinitionInput!) {
          metafieldDefinitionCreate(definition: $definition) {
            createdDefinition { id namespace key } userErrors { field message code } }}""", {"definition": {
            "name": name, "namespace": NS, "key": key, "type": typ, "ownerType": "PRODUCT",
            "validations": validations, "access": {"storefront": "PUBLIC_READ"}}})["metafieldDefinitionCreate"],
            f"metafieldDefinitionCreate {key}")


def create_fabrics():
    print("Swatch images")
    paths = {f["slug"]: os.path.join(ROOT, "swatches", f"swatch_{f['no']}_{f['slug']}.jpg") for f in FABRICS}
    # Reuse the swatch images of fabrics that already exist, so reruns don't pile up duplicate files.
    existing = gql("""query { metaobjects(type: "homestage_fabric", first: 50) { nodes { handle field(key: "swatch") { value } } } }""",
                   mutate=False)["metaobjects"]["nodes"]
    have = {m["handle"]: m["field"]["value"] for m in existing if m["field"]}
    if all(f["slug"] in have for f in FABRICS) and "--new-swatches" not in sys.argv:
        ids = [have[f["slug"]] for f in FABRICS]
    else:
        ids = new_swatch_files(paths)
    return upsert_fabrics(ids), paths


def new_swatch_files(paths):
    staged = upload(list(paths.values()), "IMAGE")
    files = gql("""mutation Files($files: [FileCreateInput!]!) {
      fileCreate(files: $files) { files { id fileStatus alt } userErrors { field message code } }}""",
        {"files": [{"originalSource": staged[paths[f["slug"]]], "contentType": "IMAGE",
                    "alt": f"{f['name']} fabric swatch"} for f in FABRICS]})["fileCreate"]
    check(files, "fileCreate")
    ids = [x["id"] for x in files["files"]]
    wait_files_ready(ids)
    return ids


def upsert_fabrics(ids):
    print("Fabrics")
    gids = {}
    for f, file_id in zip(FABRICS, ids):
        mat, care = MATERIAL[f["slug"]]
        res = gql("""mutation UpsertFabric($handle: MetaobjectHandleInput!, $metaobject: MetaobjectUpsertInput!) {
          metaobjectUpsert(handle: $handle, metaobject: $metaobject) {
            metaobject { id handle } userErrors { field message code } }}""", {
            "handle": {"type": f"{NS}_fabric", "handle": f["slug"]},
            "metaobject": {"fields": [
                {"key": "number", "value": f["no"]}, {"key": "name", "value": f["name"]},
                {"key": "colour", "value": f["colour"]}, {"key": "swatch", "value": file_id},
                {"key": "material", "value": mat}, {"key": "care", "value": care}]}})["metaobjectUpsert"]
        check(res, f"metaobjectUpsert {f['slug']}")
        gids[f["slug"]] = res["metaobject"]["id"]
    return gids


def product_set(input_):
    # Variant images must also be listed among the product's files.
    files = input_.setdefault("files", [])
    known = {f["originalSource"] for f in files}
    for v in input_.get("variants", []):
        if v.get("file") and v["file"]["originalSource"] not in known:
            files.insert(0, dict(v["file"]))
            known.add(v["file"]["originalSource"])
    res = gql("""mutation SetProduct($input: ProductSetInput!, $identifier: ProductSetIdentifiers) {
      productSet(input: $input, identifier: $identifier, synchronous: true) {
        product { id handle variants(first: 10) { nodes { id title } } } userErrors { field message code } }}""",
        {"input": input_, "identifier": {"handle": input_["handle"]}})["productSet"]
    check(res, f"productSet {input_['handle']}")
    return res["product"]


def option_and_variants(price, sku_prefix, image_for):
    options = [{"name": "Fabric", "values": [{"name": f["name"]} for f in FABRICS]}]
    variants = [{
        "optionValues": [{"optionName": "Fabric", "name": f["name"]}],
        "price": price, "sku": f"{sku_prefix}-{f['no']}",
        "inventoryPolicy": "CONTINUE", "inventoryItem": {"tracked": False},
        "file": {"originalSource": image_for(f), "contentType": "IMAGE", "alt": image_alt(f)},
    } for f in FABRICS]
    return options, variants


def image_alt(f, view="three-quarter view"):
    return f"Linden two-seat sofa in {f['name']}, {view} (3D render)"


def create_sample_product(paths):
    print("Fabric sample product")
    staged = upload(list(paths.values()), "IMAGE")
    options, variants = option_and_variants("5.00", "HS-SAMPLE", lambda f: staged[paths[f["slug"]]])
    for v, f in zip(variants, FABRICS):
        v["file"]["alt"] = f"{f['name']} fabric sample"
    return product_set({
        "title": "Fabric sample", "handle": "fabric-sample", "vendor": "HomeStage", "productType": "Fabric sample",
        "status": "ACTIVE", "tags": ["sample"],
        "descriptionHtml": "<p>A 10 × 10 cm cutting of the fabric, so you can see the real colour and feel the texture at home before you order.</p>"
                           "<p><em>HomeStage is a concept store that demonstrates product page design. Orders are not fulfilled.</em></p>",
        "productOptions": options, "variants": variants})


def create_linden(gids, sample_id):
    print("Renders and 3D models")
    renders = {(f["slug"], v): os.path.join(ROOT, "renders", f"linden_{f['slug']}_{v}.jpg")
               for f in FABRICS for v in ("34", "front", "side")}
    models = {f["slug"]: os.path.join(ROOT, "models", f"linden_{f['slug']}.glb") for f in FABRICS}
    r_urls = upload(list(renders.values()), "IMAGE")
    m_urls = upload(list(models.values()), "MODEL_3D")

    print("Linden product")
    options, variants = option_and_variants("2180.00", "HS-LINDEN",
                                            lambda f: r_urls[renders[(f["slug"], "34")]])
    views = {"front": "front view", "side": "side view"}
    files = [{"originalSource": r_urls[renders[(f["slug"], v)]], "contentType": "IMAGE",
              "alt": image_alt(f, views[v])} for f in FABRICS for v in ("front", "side")]
    files += [{"originalSource": m_urls[models[f["slug"]]], "contentType": "MODEL_3D",
               "alt": f"Linden two-seat sofa in {f['name']}, 3D model"} for f in FABRICS]
    dim = lambda value: json.dumps({"value": value, "unit": "INCHES"})
    metafields = [
        {"namespace": NS, "key": "fabrics", "type": "list.metaobject_reference",
         "value": json.dumps([gids[f["slug"]] for f in FABRICS])},
        {"namespace": NS, "key": "width", "type": "dimension", "value": dim(62)},
        {"namespace": NS, "key": "depth", "type": "dimension", "value": dim(26)},
        {"namespace": NS, "key": "height", "type": "dimension", "value": dim(31)},
        {"namespace": NS, "key": "lead_time_min_weeks", "type": "number_integer", "value": "6"},
        {"namespace": NS, "key": "lead_time_max_weeks", "type": "number_integer", "value": "8"},
        {"namespace": NS, "key": "making_stages", "type": "list.single_line_text_field", "value": json.dumps(STAGES)},
        {"namespace": NS, "key": "sample_product", "type": "product_reference", "value": sample_id},
    ]
    return product_set({
        "title": "Linden two-seat sofa", "handle": "linden-sofa", "vendor": "HomeStage", "productType": "Sofa",
        "status": "ACTIVE", "tags": ["sofa", "made to order"],
        "descriptionHtml": "<p>A two-seat sofa with a carved, hand-finished wood frame and a deep sprung seat. "
                           "Made to order in your choice of six fabrics.</p>"
                           "<p>Every image is a 3D render of the actual model. Use View in your room to see it at true size.</p>"
                           "<p><em>HomeStage is a concept store that demonstrates product page design. Orders are not fulfilled.</em></p>",
        "productOptions": options, "variants": variants, "files": files, "metafields": metafields})


def publish(product_ids):
    pubs = gql("query { publications(first: 10) { nodes { id catalog { title } } } }", mutate=False)["publications"]["nodes"]
    online = next(p["id"] for p in pubs if p["catalog"]["title"].endswith("Online Store"))
    for pid in product_ids:
        check(gql("""mutation Publish($id: ID!, $input: [PublicationInput!]!) {
          publishablePublish(id: $id, input: $input) { userErrors { field message } }}""",
            {"id": pid, "input": [{"publicationId": online}]})["publishablePublish"], "publishablePublish")
    print("Published to Online Store")


if __name__ == "__main__":
    define_types()
    gids, paths = create_fabrics()
    sample = create_sample_product(paths)
    linden = create_linden(gids, sample["id"])
    publish([sample["id"], linden["id"]])
    print(json.dumps({"linden": linden, "sample": sample}, indent=1))
