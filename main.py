import os
import zipfile
import shutil
import json

if not os.path.isdir("dist"):
    os.mkdir("dist")

datapackpath = input("Enter the filename to the datapack (must be .zip):")
if not os.path.exists(os.path.join(os.getcwd(), datapackpath)):
    print("Datapack does not exist")
    exit()
shutil.copyfile(
    os.path.join(os.getcwd(), datapackpath),
    os.path.join("dist", os.path.basename(datapackpath)),
)
with zipfile.ZipFile(
    os.path.join("dist", os.path.basename(datapackpath)), "a"
) as zip_ref:
    modloader = input("Enter Modloader, 1 for Fabric or 2 for Neoforge:")
    if modloader == "1":
        with zipfile.ZipFile(
            os.path.join(os.getcwd(), datapackpath), "r"
        ) as packmcmetazip:
            packmcmeta = json.load(packmcmetazip.open("pack.mcmeta"))
            description = packmcmeta["pack"]["description"]
        name = input("What is the name of your mod?:")
        modid = input("What is the id of your mod? (must have no spaces):")
        author = input("Who is the author of your mod?:")
        version = input(
            "What is the version of your mod? (NOT what mc version you're targeting):"
        )
        mcversion = input("What version of Minecraft are you targeting?:")
        data = {
            "schemaVersion": 1,
            "id": modid,
            "version": version,
            "name": name,
            "description": description,
            "authors": [author],
            "depends": {"fabricloader": ">=0.15.0", "minecraft": [mcversion]},
        }
        zip_ref.writestr(
            "fabric.mod.json", json.dumps(data, indent=2)
        )  # add data from input here
    elif modloader == "2":
        name = input("What is the name of your mod?:")
        modid = input("What is the id of your mod? (must have no spaces):")
        license = input("What is the license of your mod? (e.g., MIT, CC-BY-NC-4.0):")
        version = input(
            "What is the version of your mod? (NOT what mc version you're targeting):"
        )
        with zipfile.ZipFile(
            os.path.join(os.getcwd(), datapackpath), "r"
        ) as packmcmetazip:
            packmcmeta = json.load(packmcmetazip.open("pack.mcmeta"))
            description = packmcmeta["pack"]["description"]
        versionrange = input(
            "What is your Minecraft version range (e.g. 1.21.11,26.1.2):"
        )
        zip_ref.writestr(
            "META-INF/neoforge.mods.toml",
            f"""
modLoader = "javafml"
loaderVersion = "[1,)"
license = "{license}"

[[mods]]
modId = "{modid}"
version = "{version}"
displayName = "{name}"
description = "{description}"

[[dependencies.{modid}]]
modId = "minecraft"
type = "required"
versionRange = "[{versionrange}]"
""",
        )
    else:
        print("Invalid modloader")
        exit()
os.rename(
    os.path.join("dist", os.path.basename(datapackpath)),
    os.path.join("dist", f"{modid}-{version}.jar"),
)
