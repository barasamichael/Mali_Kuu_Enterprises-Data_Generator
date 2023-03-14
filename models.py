from sqlalchemy import (create_engine, Column, DateTime, Integer, String, Boolean, 
        Text, DECIMAL, TIMESTAMP, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from config import Config

# acquire environment variables
db_host = Config.DB_HOST
db_user = Config.DB_USER
db_password = Config.DB_PASSWORD
db_name = Config.DB_NAME

# Construct MySQL database URL
mysql_url = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(mysql_url)
Base = declarative_base()


class Role(Base):
    __tablename__ = 'tbl_Role'

    roleId = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    permissions = Column(Integer, default=0)
    dateCreated = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    lastUpdated = Column(TIMESTAMP, 
            server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')


class Item(Base):
    __tablename__ = 'tbl_Item'

    itemId = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    dateCreated = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    lastUpdated = Column(TIMESTAMP, 
            server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')


class Customer(Base):
    __tablename__ = 'tbl_Customer'

    customerId = Column(Integer, primary_key=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    middleName = Column(String(255))
    gender = Column(String(127), nullable=False)
    emailAddress = Column(String(255), nullable=False)
    phoneNumber = Column(String(255), nullable=False)
    active = Column(Boolean, default=True)
    locationAddress = Column(Text, nullable=False)
    passcode = Column(String(255), default='password', nullable=False)
    dateCreated = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    lastUpdated = Column(TIMESTAMP, 
            server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')


class Supplier(Base):
    __tablename__ = 'tbl_Supplier'

    supplierId = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    specialty = Column(String(255), nullable=False)
    emailAddress = Column(String(255), nullable=False)
    phoneNumber = Column(String(255), nullable=False)
    locationAddress = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
    passcode = Column(String(255), nullable=False)
    dateCreated = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    lastUpdated = Column(TIMESTAMP, 
            server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')


class User(Base):
    __tablename__ = 'tbl_User'

    userId = Column(Integer, primary_key=True)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    middleName = Column(String(255))
    gender = Column(String(127), nullable=False)
    emailAddress = Column(String(255), nullable=False)
    phoneNumber = Column(String(255), nullable=False)
    nationalID = Column(String(127), nullable=False)
    locationAddress = Column(String(255))
    active = Column(Boolean, default=True)
    passcode = Column(String(255), nullable=False)
    roleId = Column(Integer, ForeignKey('tbl_Role.roleId'), nullable=False)
    dateCreated = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    lastUpdated = Column(TIMESTAMP, 
            server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')


class ItemInstance(Base):
    __tablename__ = 'tbl_ItemInstance'
    itemInstanceId = Column(Integer, primary_key=True, autoincrement=True)
    buyingPrice = Column(DECIMAL(10,2), nullable=False)
    sellingPrice = Column(DECIMAL(10,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    present = Column(Boolean, default=True)
    itemId = Column(Integer, ForeignKey('tbl_Item.itemId'), nullable=False)
    supplyId = Column(Integer, ForeignKey('tbl_Supply.supplyId'), nullable=False)
    dateCreated = Column(DateTime, default=datetime.utcnow, nullable=False)
    lastUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
            nullable=False)
    item = relationship("Item")
    supply = relationship("Supply")


class Order(Base):
    __tablename__ = 'tbl_Order'
    orderId = Column(Integer, primary_key=True, autoincrement=True)
    payment = Column(String(127), nullable=False)
    completed = Column(Boolean, default=False)
    customerId = Column(Integer, ForeignKey('tbl_Customer.customerId'), nullable=False)
    dateCreated = Column(DateTime, default=datetime.utcnow, nullable=False)
    lastUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
            nullable=False)
    customer = relationship("Customer")


class Supply(Base):
    __tablename__ = 'tbl_Supply'
    supplyId = Column(Integer, primary_key=True, autoincrement=True)
    payment = Column(String(127), nullable=False)
    completed = Column(Boolean, default=False)
    supplierId = Column(Integer, ForeignKey('tbl_Supplier.supplierId'), nullable=False)
    dateCreated = Column(DateTime, default=datetime.utcnow, nullable=False)
    lastUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
            nullable=False)
    supplier = relationship("Supplier")


class OrderAssignment(Base):
    __tablename__ = 'tbl_OrderAssignment'
    orderAssignmentId = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    orderId = Column(Integer, ForeignKey('tbl_Order.orderId'), nullable=False)
    itemInstanceId = Column(Integer, ForeignKey('tbl_ItemInstance.itemInstanceId'), 
            nullable=False)
    dateCreated = Column(DateTime, default=datetime.utcnow, nullable=False)
    lastUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, 
            nullable=False)
    order = relationship("Order")
    itemInstance = relationship("ItemInstance")
