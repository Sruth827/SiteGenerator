from textnode import TextNode, TextType 

def main(): 
    newnode = TextNode("this is some anchor text", TextType.LINK, "https://www.sean.com/")
    print(newnode)





if __name__ == "__main__":
    main()

