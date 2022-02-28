import requests, subprocess, os, fpdf, shutil, cv2

print("PearsonDownloader+ by cyxv\n")
urlid = input("URL ID: ")
bookid = input("Book ID: ")

urlString = "https://{}.cloudfront.net/resources/products/epubs/generated/{}/foxit-assets/pages/page{}?password=&accessToken=null&formMode=true"

if os.path.exists("workspace"):
    if len(os.listdir("workspace")) != 0:
        print("Workspace folder not empty! Clearing...")
        for i in os.listdir("workspace"): os.remove(os.path.join("workspace", i))
else:
    print("Workspace folder not found, creating.")
    os.mkdir("workspace")

pagenum = 0
while True:
    i = requests.get(urlString.format(urlid, bookid, pagenum))
    if i.status_code == 403:
        print("Done downloading pages.")
        del i
        break
    elif i.status_code == 200:
        img = requests.get(urlString.format(urlid, bookid, pagenum), stream=True)
        with open("workspace/{}.png".format(pagenum), "wb") as out_file:
            shutil.copyfileobj(img.raw, out_file)
        print("Downloaded page {}".format(pagenum))
        del img
    del i
    pagenum += 1

p0 = cv2.imread("workspace/0.png")
height, width = p0.shape[:2]
del p0
print("Pages are {}x{} each.".format(height, width))

pages = [i for i in os.listdir("workspace")]
print("Now converting pages to PDF.")
pdf = fpdf.FPDF("P", "pt", (width/0.75, height/0.75))

for i in sorted([int(x[:-4]) for x in pages]):
    pdf.add_page()
    pdf.image("workspace/{}.png".format(i), w=width/0.75, h=height/0.75, x=0, y=0)
    print("Added {} to document".format(i))

print("Outputting...")
pdf.output("output.pdf")
print("Outputted to output.pdf. Enjoy :)")
subprocess.run("pause", shell=True)
