import threading
import time, os
import random
from faker import Faker
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from models import (Role, Customer, Order, OrderAssignment, Item, ItemInstance, 
        Supplier, Supply, User)
from config import Config

class TimeGenerator:
    def __init__(self):
        self.timestamp = datetime(2020, 12, 12)

    def run(self):
        while True:
            # Increment time by a random number of seconds
            increment = random.randint(2400, 12000)
            self.timestamp += timedelta(seconds = increment)
            time.sleep(0.1)

            # ensure the loop is not infinite
            if self.timestamp >= datetime.now():
                break

class DataGenerator:
    def __init__(self, time_generator):
        self.time_incrementer = time_generator

        # acquire environment variables
        db_host = Config.DB_HOST
        db_user = Config.DB_USER
        db_password = Config.DB_PASSWORD
        db_name = Config.DB_NAME

        # Construct MySQL database URL
        mysql_url = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"

        self.engine = create_engine(mysql_url)
        self.Session = sessionmaker(bind = self.engine)
        self.session = self.Session()
        self.faker = Faker()
        
    def generateRoles(self):
        """
        Generates roles
        """
        from roles import roles
        
        for index in range(len(roles) - 1):
            role = Role(
                    title = roles[index][0],
                    description = roles[index][1], 
                    permissions = roles[index][2],
                    dateCreated = self.time_incrementer.timestamp,
                    lastUpdated = self.time_incrementer.timestamp
            )
            self.session.add(role)
            self.session.commit()
            print(self.time_incrementer.timestamp, "Role added successfully...")


    def generateCustomer(self):
        """
        Generates a customer
        """
        customer = Customer(
                firstName = self.faker.first_name(), 
                lastName = self.faker.last_name(), 
                middleName = self.faker.first_name(),
                gender = random.choice(['Male', 'Female']), 
                emailAddress = self.faker.email(), 
                phoneNumber = self.faker.phone_number(),
                locationAddress = self.faker.address(), 
                passcode = self.faker.password(),
                dateCreated = self.time_incrementer.timestamp,
                lastUpdated = self.time_incrementer.timestamp
                )
        self.session.add(customer)
        self.session.commit()
        print(self.time_incrementer.timestamp, "Customer added successfully...")


    def generateUser(self):
        """
        Generate a user
        """
        user = User(
                firstName = self.faker.first_name(), 
                lastName = self.faker.last_name(), 
                middleName = self.faker.first_name(),
                gender = random.choice(['Male', 'Female']), 
                emailAddress = self.faker.email(),
                phoneNumber = self.faker.phone_number(),
                nationalID = self.faker.ssn(), 
                locationAddress = self.faker.address(), 
                passcode = self.faker.password(),
                roleId = random.randint(1, self.session.query(Role).count()),
                dateCreated = self.time_incrementer.timestamp,
                lastUpdated = self.time_incrementer.timestamp
                )
        self.session.add(user)
        self.session.commit()
        print(self.time_incrementer.timestamp, "User added successfully...")


    def generateSupplier(self):
        """
        Generates a supplier
        """
        supplier = Supplier(
                name = self.faker.company(), 
                specialty = self.faker.word(), 
                emailAddress = self.faker.email(), 
                phoneNumber = self.faker.phone_number(),
                locationAddress = self.faker.address(), 
                passcode = self.faker.password(),
                dateCreated = self.time_incrementer.timestamp,
                lastUpdated = self.time_incrementer.timestamp
                )
        self.session.add(supplier)
        self.session.commit()
        print(self.time_incrementer.timestamp, "Supplier added successfully...")


    def generateItem(self):
        """
        Generates an item
        """
        from products import products
        
        for index in range(len(products) - 1):
            item = Item(
                name = products[index][0], 
                description = products[index][1],
                dateCreated = self.time_incrementer.timestamp,
                lastUpdated = self.time_incrementer.timestamp
                )
            self.session.add(item)
            self.session.commit()
            print(self.time_incrementer.timestamp, "Item added successfully...")


    def generateSupply(self):
        """
        Generates a supply
        """
        supply = Supply(
                payment = random.choice([ 
                    "Cash", "Credit Card", "Debit Card", "Cheque", "Bond"]), 
                completed = random.randint(1, 120) < 100,
                supplierId = random.randint(1, self.session.query(Supplier).count()),
                dateCreated = self.time_incrementer.timestamp,
                lastUpdated = self.time_incrementer.timestamp
                )
        self.session.add(supply)
        self.session.commit()
        print(self.time_incrementer.timestamp, "Supply added successfully...")

    
    def generateItemInstance(self):
        """
        Generates an item instance
        """
        bp = random.randint(1000, 100000)
        sp = bp + random.randint(500, 50000)

        item_instance = ItemInstance(
                buyingPrice = bp,
                sellingPrice = sp,
                quantity = random.randint(20, 50),
                itemId = random.randint(1, self.session.query(Item).count()),
                supplyId = random.randint(1, self.session.query(Supply).count()),
                dateCreated = self.time_incrementer.timestamp,
                lastUpdated = self.time_incrementer.timestamp
                )
        self.session.add(item_instance)
        self.session.commit()
        print(self.time_incrementer.timestamp, "ItemInstance added successfully...")


    def generateOrder(self):
        """
        Generates an order
        """
        order = Order(
                payment = random.choice([
                    "Cash", "Credit Card", "Debit Card", "Cheque", "Bond"]), 
                completed = random.randint(1, 105) < 100, 
                customerId = random.randint(1, self.session.query(Customer).count()),
                dateCreated = self.time_incrementer.timestamp,
                lastUpdated = self.time_incrementer.timestamp
                )
        self.session.add(order)
        self.session.commit()
        print(self.time_incrementer.timestamp, "Order added successfully...")

        
    def generateOrderAssignment(self):
        """
        Generates an order assignment with a quantity that does not exceed the 
        quantity in the corresponding item instance
        """
        # get a random item instance
        item_instance = self.session.query(ItemInstance).offset(
                random.randint(0, self.session.query(ItemInstance).count() - 1)).first()

        if item_instance.present == False:
            return

        # calculate the max quantity for the order assignment
        sold_quantity = self.session.query(func.sum(OrderAssignment.quantity)).filter(
                        OrderAssignment.itemInstanceId == item_instance.itemInstanceId).scalar()
        
        if not sold_quantity:
            sold_quantity = 0
        
        max_quantity = item_instance.quantity - sold_quantity

        if max_quantity < 1:
            print(self.time_incrementer.timestamp, "No available quantity for item instance %d" % item_instance.itemInstanceId)
            item_instance.present = False

            self.session.add(item_instance)
            self.session.commit()
            return

        # generate the order assignment with a random quantity
        quantity = random.randint(1, max_quantity)
        order_assignment = OrderAssignment(
            quantity = quantity,
            orderId = random.randint(1, self.session.query(Order).count()),
            itemInstanceId = item_instance.itemInstanceId,
            dateCreated = self.time_incrementer.timestamp,
            lastUpdated = self.time_incrementer.timestamp
        )
        self.session.add(order_assignment)
        self.session.commit()
        print(self.time_incrementer.timestamp, "OrderAssignment added successfully...")

    def run(self):
        """
        Controls generation of records
        """
        # generate employee roles
        self.generateRoles()

        # generate products
        self.generateItem()
        
        # counters
        counter = 0
        
        # loop
        while True:
            if counter % 20 == 0:
                for index in range(random.randint(10, 20)):
                    self.generateUser()

            if counter % 20 == 0:
                for i in range(random.randint(10, 15)):
                    self.generateSupplier()
                    self.generateSupply()

                for i in range(random.randint(200, 300)):
                    self.generateItemInstance()

            if counter % 2 == 0:
                for index in range(random.randint(20, 30)):
                    self.generateCustomer()
                    for i in range(random.randint(20, 30)):
                        self.generateOrder()

                for i in range(random.randint(100, 150)):
                    self.generateOrderAssignment()

            for i in range(random.randint(100, 150)):
                self.generateOrder()

            for i in range(random.randint(500, 1000)):
                self.generateOrderAssignment()

            for i in range(random.randint(5, 10)):
                self.generateSupply()
            
            for i in range(random.randint(500, 1000)):
                self.generateOrderAssignment()

            for i in range(random.randint(200, 400)):
                self.generateItemInstance()

            for i in range(random.randint(150, 200)):
                self.generateOrderAssignment()

            # ensure the loop is not infinite
            if self.time_incrementer.timestamp >= datetime.now():
                break

            counter += 1

class App:
    def __init__(self):
        self.time_generator = TimeGenerator()
        self.data_generator = DataGenerator(self.time_generator)

    def run(self):
        # Start time generator thread
        time_thread = threading.Thread(target=self.time_generator.run)
        time_thread.daemon = True
        time_thread.start()

        # Start data generator thread
        data_thread = threading.Thread(target=self.data_generator.run)
        data_thread.daemon = True
        data_thread.start()

        # Wait for threads to complete
        time_thread.join()
        data_thread.join()

if __name__ == '__main__':
	app = App()
	app.run()
