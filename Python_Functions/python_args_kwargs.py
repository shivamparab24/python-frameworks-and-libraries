# def tea_order(customer_name, tea_type, milk = None, sweetner = None):
#     print(customer_name, "ordered a", tea_type, "taa")
#     if milk != None:
#         print(" - Add: ", milk)
#     if sweetner != None:
#         print(" - Add: ", sweetner)


# tea_order("Alice", "chamomile")
# tea_order("Bob", "Black", "Oat")
# tea_order("Tony", "Black", "Oat", "Honey")



# def tea_order(customer_name, tea_type, *extra):
#     print(customer_name, "ordered a", tea_type, "taa")

#     for arg in extra:
#         print(" - Add: ", arg)


# tea_order("Alice", "chamomile")
# tea_order("Bob", "Black", "Oat")
# tea_order("Tony", "Black", "Oat", "Honey")




# def tea_order(customer_name, tea_type, **extrass):
#     print(customer_name, "ordered a", tea_type, "taa")

#     for key, value in extrass.items():
#         print(" - Add: ", key, " : ", value)

# tea_order("Alice", "chamomile")
# tea_order("Bob", "Black", milk = "Oat")
# tea_order("Tony", "Black", milk = "Oat", sweetner = "Honey")



def tea_order(customer_name, tea_type,*args, **extrass):
    print(customer_name, "ordered a", tea_type, "taa")

    for arg in args:
        print(" - Add: ", arg)

    for key, value in extrass.items():
        print(" - Add: ", key, " : ", value)


eve_extra = {"milk": "almond", "sweetner": "sugar", "flavor": "lemon"}

tea_order("Eve", "Green", milk = "almond", sweetner = "sugar", flavor = "lemon")
tea_order("Eve", "Green", **eve_extra)
print()
tea_order("Alice", "chamomile") 
tea_order("Bob", "Black", milk = "Oat")
tea_order("Tony", "Black", "Oat", sweetner = "Honey")

