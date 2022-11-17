



from PIL import Image




img = Image.open( r"C:\Users\upaay\OneDrive\Desktop\1569.png")

size = (225, 150)

img.resize(size)


img.show()
