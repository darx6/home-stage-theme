"""Small helpers around `shopify store execute` for setting up HomeStage demo data."""
import json, mimetypes, os, subprocess, tempfile, time, urllib.request, uuid

STORE = "homestage-uqutijpv.myshopify.com"
API_VERSION = "2026-10"


def gql(query, variables=None, mutate=True):
    """Run one Admin GraphQL operation through the Shopify CLI and return its data."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as vf:
        json.dump(variables or {}, vf)
    cmd = ["shopify", "store", "execute", "--store", STORE, "--version", API_VERSION,
           "--query", query, "--variable-file", vf.name, "--json"]
    if mutate:
        cmd.append("--allow-mutations")
    res = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(vf.name)
    out = res.stdout[res.stdout.find("{"):]
    if res.returncode or not out:
        raise RuntimeError(f"CLI failed: {res.stderr.strip() or res.stdout.strip()}")
    return json.loads(out)


def check(payload, name):
    """Raise on userErrors, except 'already exists' so reruns are safe."""
    errs = payload.get("userErrors") or []
    real = [e for e in errs if e.get("code") not in ("TAKEN", "UNIQUE_KEY_VIOLATION")]
    if real:
        raise RuntimeError(f"{name}: {real}")
    return payload


def upload(paths, resource):
    """Stage and upload local files; return {path: resourceUrl}."""
    inputs = [dict(filename=os.path.basename(p), mimeType=mime(p), resource=resource,
                   fileSize=str(os.path.getsize(p)), httpMethod="POST") for p in paths]
    data = gql("""mutation Stage($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets { url resourceUrl parameters { name value } }
        userErrors { field message }
      }}""", {"input": inputs})["stagedUploadsCreate"]
    check(data, "stagedUploadsCreate")
    urls = {}
    for p, t in zip(paths, data["stagedTargets"]):
        post_multipart(t["url"], [(x["name"], x["value"]) for x in t["parameters"]], p)
        urls[p] = t["resourceUrl"]
        print("  uploaded", os.path.basename(p))
    return urls


def mime(path):
    return "model/gltf-binary" if path.endswith(".glb") else mimetypes.guess_type(path)[0]


def post_multipart(url, fields, path):
    boundary = uuid.uuid4().hex
    body = b""
    for k, v in fields:
        body += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    body += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{os.path.basename(path)}"\r\n'
             f"Content-Type: {mime(path)}\r\n\r\n").encode() + open(path, "rb").read() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        if r.status >= 300:
            raise RuntimeError(f"upload {path}: HTTP {r.status}")


def wait_files_ready(ids, timeout=180):
    """Poll until uploaded files finish processing."""
    end = time.time() + timeout
    while time.time() < end:
        nodes = gql("""query F($ids: [ID!]!) { nodes(ids: $ids) { ... on File { id fileStatus } } }""",
                    {"ids": ids}, mutate=False)["nodes"]
        status = {n["id"]: n["fileStatus"] for n in nodes if n}
        if any(s == "FAILED" for s in status.values()):
            raise RuntimeError(f"file processing failed: {status}")
        if all(s == "READY" for s in status.values()):
            return
        time.sleep(3)
    raise RuntimeError("files not ready in time")
