def make_food(callback):
    food = "Pizza"
    callback(food)


def put_food_in_bag(food):
    print(f"{food} is in the bag")


def put_food_in_fridge(food):
    print(f"{food} is in the fridge")


def give_me_food_to_eat(food):
    print(f"Here is your {food} to eat")


make_food(put_food_in_bag)
make_food(put_food_in_fridge)
make_food(give_me_food_to_eat)