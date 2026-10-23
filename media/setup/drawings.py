"""Replace a product's front and side outline drawings, removing the previous drawing files.

Run from the repo root: python3 -I media/setup/drawings.py linden-sofa media/linden/drawings
"""
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from shop import gql, check, upload, wait_files_ready

handle, folder = sys.argv[1], sys.argv[2]
product = gql("""query P($h: String!) { productByHandle(handle: $h) { id title
  front: metafield(namespace: "homestage", key: "drawing_front") { value }
  side: metafield(namespace: "homestage", key: "drawing_side") { value } } }""", {"h": handle}, mutate=False)["productByHandle"]
old = [m["value"] for m in (product["front"], product["side"]) if m]

paths = {v: os.path.join(folder, f"drawing_{v}.png") for v in ("front", "side")}
staged = upload(list(paths.values()), "IMAGE")
created = gql("""mutation Files($files: [FileCreateInput!]!) {
  fileCreate(files: $files) { files { id } userErrors { field message code } }}""",
    {"files": [{"originalSource": staged[paths[v]], "contentType": "IMAGE",
                "alt": f"{product['title']}, {v} outline drawing"} for v in ("front", "side")]})["fileCreate"]
check(created, "fileCreate")
ids = dict(zip(("front", "side"), [f["id"] for f in created["files"]]))
wait_files_ready(list(ids.values()))

check(gql("""mutation SetFields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) { metafields { key value } userErrors { field message code } } }""",
    {"metafields": [{"ownerId": product["id"], "namespace": "homestage", "key": f"drawing_{v}",
                     "type": "file_reference", "value": ids[v]} for v in ("front", "side")]})["metafieldsSet"], "metafieldsSet")

if old:
    check(gql("""mutation Del($fileIds: [ID!]!) { fileDelete(fileIds: $fileIds) { deletedFileIds userErrors { field message code } } }""",
              {"fileIds": old})["fileDelete"], "fileDelete")
print("drawings replaced", ids, "removed", len(old))
