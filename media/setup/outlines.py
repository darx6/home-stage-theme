"""Store a product's traced front and side silhouettes as JSON fields the theme draws in ink,
and retire the earlier raster drawing fields and files.

Run from the repo root: python3 -I media/setup/outlines.py linden-sofa media/linden/outlines
The path files come from trace.cjs (potrace) run on the silhouette PNGs in the same folder.
"""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from shop import gql, check

handle, folder = sys.argv[1], sys.argv[2]
NS = "homestage"


def main_contour(d):
    # potrace returns every closed contour; keep the outer silhouette (the longest one).
    parts = [p.strip() for p in re.split(r"(?=M)", d) if p.strip()]
    return max(parts, key=len)


product = gql("""query P($h: String!) { productByHandle(handle: $h) { id
  front: metafield(namespace: "homestage", key: "drawing_front") { id value }
  side: metafield(namespace: "homestage", key: "drawing_side") { id value } } }""", {"h": handle}, mutate=False)["productByHandle"]

for key, name in (("outline_front", "Front outline"), ("outline_side", "Side outline")):
    check(gql("""mutation CreateFieldDef($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) { createdDefinition { id } userErrors { field message code } }}""",
        {"definition": {"name": name, "namespace": NS, "key": key, "type": "json", "ownerType": "PRODUCT",
                        "access": {"storefront": "PUBLIC_READ"}}})["metafieldDefinitionCreate"], f"definition {key}")

values = []
for v in ("front", "side"):
    p = json.load(open(os.path.join(folder, f"path_{v}.json")))
    values.append({"ownerId": product["id"], "namespace": NS, "key": f"outline_{v}", "type": "json",
                   "value": json.dumps({"width": p["w"], "height": p["h"], "d": main_contour(p["d"])})})
check(gql("""mutation SetFields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) { metafields { key } userErrors { field message code } } }""",
    {"metafields": values})["metafieldsSet"], "metafieldsSet")

old_files = [m["value"] for m in (product["front"], product["side"]) if m]
if old_files:
    check(gql("""mutation DeleteFields($metafields: [MetafieldIdentifierInput!]!) {
      metafieldsDelete(metafields: $metafields) { deletedMetafields { key } userErrors { field message } } }""",
        {"metafields": [{"ownerId": product["id"], "namespace": NS, "key": k} for k in ("drawing_front", "drawing_side")]})["metafieldsDelete"], "metafieldsDelete")
    check(gql("""mutation Del($fileIds: [ID!]!) { fileDelete(fileIds: $fileIds) { deletedFileIds userErrors { field message code } } }""",
              {"fileIds": old_files})["fileDelete"], "fileDelete")
for key in ("drawing_front", "drawing_side"):
    res = gql("""mutation DeleteDef($identifier: MetafieldDefinitionIdentifierInput!) {
      metafieldDefinitionDelete(identifier: $identifier, deleteAllAssociatedMetafields: true) {
        deletedDefinitionId userErrors { field message code } } }""",
        {"identifier": {"ownerType": "PRODUCT", "namespace": NS, "key": key}})["metafieldDefinitionDelete"]
    if res["userErrors"] and not any(e.get("code") == "NOT_FOUND" for e in res["userErrors"]):
        raise RuntimeError(res["userErrors"])
print("outlines set; removed", len(old_files), "raster drawings")
