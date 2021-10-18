import csv
import os
import json
import random

# get unsold tokens with smartcontract functions, result : 
unsoldTokens = ["83","97","166","233","256","271","288","297","298","314","324","357","375","382","395","403","415","522","555","601","603","612","640","705","708","720","744","783","785","796","850","870","908","932","949","982","1022","1044","1220","1252","1288","1297","1327","1331","1347","1360","1391","1421","1466","1517","1639","1640","1661","1664","1697","1849","1850","1909","1910","1915","1916","1957","1958","1985","1986","2091","2092","2145","2146","2197","2198","2217","2218","2409","2410","2431","2432","2479","2480","2513","2514","2693","2694","2697","2698","2741","2742","2805","2806","2807","2808","2911","2912","2947","2948","2953","2954","3141","3142","3161","3162","3333","3334","3349","3350","3351","3352","3353","3354","3443","3444","3463","3464","3529","3530","3541","3542","3669","3670","3817","3818","3891","3892","3901","3902","3917","3918","3931","3932","4009","4010","4041","4042","4063","4064","4067","4068","4121","4122","4163","4164","4277","4278","4289","4290","4387","4388","4421","4422","4461","4462","4499","4500","4543","4544","4553","4554","4583","4584","4841","4842","4871","4872","4937","4938","5055","5056","5137","5138","5171","5172","5201","5202","5307","5308","5321","5322","5329","5330","5381","5382","5421","5422","5475","5476","5527","5528","5569","5570","5679","5680","5707","5708","5855","5856","6019","6020","6123","6124","6225","6226","6339","6340","6439","6440","6471","6472","6477","6478","6565","6566","6649","6650","6741","6742","6825","6826","6907","6908","7027","7028","7033","7034","7055","7056","7099","7100","7249","7250","7271","7272","7277","7278","7367","7368","7407","7408","7411","7412","7475","7476","7549","7550","7603","7604","7611","7612","7641","7642","7655","7656","7769","7770","7815","7816","7995","7996","8029","8030","8091","8092","8115","8116","8119","8120","8171","8172","8179","8180","8187","8188","8301","8302","8315","8316","8391","8392","8431","8432","8459","8460","8471","8472","8533","8534","8569","8570","8609","8610","8689","8690","8693","8694","8829","8830"]

# create Metadata dict with GoogleSheets metadata
metadata = []

# parse key value metadata CSV file
with open(f"./MEKA NAMES - OG.csv", encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_reader = list(csv_reader)
    line_count = 0

    for i in range(0,38,2):
        rowCount = 0
        data = {}
        for row in csv_reader:
            if rowCount == 4:
                data = {
                    "name":row[i+1],
                    "values":{}
                }
            if rowCount >= 5:
                if row[i] == "" and row[i+1] == "": continue
                data["values"][row[i]] = row[i+1]

            rowCount += 1

        metadata.append(data)

# load pictures folder
images = os.listdir(f"./output/")

# run random
random.seed(561)
random.shuffle(images)

# create global variable
imagesCreate = {}
globalMetadata = {}
error = 0
token = 1
unsold = 0

# for each images
for image in images:
    
    # remove placeholder from the file list
    if image in ["1080_placeholder.gif"]:
        continue

    # parse file name to get metadatas key
    data = image.split("_")

    # create hash to test the uniqueness of each image
    hash = ""
    for k in range(len(data)-1):
        hash += data[k]+"_"
    
    # test uniqueness and show error if
    if hash in imagesCreate:
        for imgHash in imagesCreate:
            if imgHash == hash and data[0] != "Legendary" :
                theOriginal = imagesCreate[imgHash]
                print(f'ERROR [{error}] | dup : {image} | orignal : {theOriginal}')
                error += 1
                break
    else:
        imagesCreate[hash] = image
    
    # parse metadatas key / values
    fImage = image
    attributes = []
    for key in range(len(data) - 1):
        try:
            trait = metadata[key]["name"]
   
            # set legendary placeholder traits
            if data[key] == "Legendary":
                attributes.append({
                    "trait_type":"Status",
                    "value":"Hidden"
                })
                break
            
            # unsold token (set the placeholder and no metadata)
            if str(token) in unsoldTokens:
                attributes.append({
                    "trait_type":"Status",
                    "value":"Hidden"
                })
                fImage = "1080_placeholder.gif"
                unsold += 1
                print(f"Image unsold : {image}")
                break
            
            # dont add trait for color none
            if trait == "Color" and data[key] == "none":
                continue
            
            value = metadata[key]["values"][data[key]]

            skip = False
            # skip same color in metadata (only once unique color)
            for att in attributes:
                if att["trait_type"] == trait and att["value"] == value:
                    skip = True
            
            # show error for Meka with metadata POUBELLE
            if value == "POUBELLE":
                print(f'ERROR [{error}] | image POUBELLE | image : {image}')
                error += 1
            
            # If the metadata is not found in the Google Sheets, show error
            if value == "" and data[key] != "0":
                if metadata[key]["name"] != "Background":
                    print(f'ERROR [{error}] | value empty | trait : `{metadata[key]["name"]}` | image : `{Fimage}`')
                    error += 1
            
            # if value is empty or 0, skip metadata
            if value == "" and data[key] == "0":
                skip = True

            if skip: continue
            
            # set attribute key value
            attributes.append({
                "trait_type":trait,
                "value":value
            })
        except:
            # show error
            if metadata[key]["name"] != "Background":
                print(f'ERROR [{error}] | key `{data[key]}` introuvable | trait : `{metadata[key]["name"]}` | image : `{Fimage}`')
                error += 1
    
    # add meka in global metadata JSON
    globalMetadata[token] = {
        "id":token,
        "image":f"https://img.themekaverse.com/{fImage}",
        "attributes":attributes
    }

    # next token
    token += 1

# save the json file
with open(f"./generation.json", 'w') as f:
    json.dump(globalMetadata, f,  indent=2)
    
print("------------------------------------------------------------------------------------------")
print(f"Token : {(token - 1)}")
print(f"Unsold : {unsold}")
print(f"Errors : {error}")
print("------------------------------------------------------------------------------------------")
