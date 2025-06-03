import pytest


# Test to check equality and inequality assertions
def test_equal_not_equal():
    assert 3 == 3  # This will pass since 3 equals 3
    assert 3 != 5  # This will pass since 3 is not equal to 5


# Test to check boolean conditions
def test_bool():
    x = True
    assert x is True  # Confirms x is True
    assert ("hello" == "world") is False  # False because strings don't match
    assert ("hello" == "hello") is True  # True because strings match


# Test to check types using the 'is' operator (note: these are incorrect usage)
def test_type():
    # The following lines use `type(...)` incorrectly and will not test the type of the string.
    assert type("Hello" is str)
    assert type("Hello" is not int)
    assert type("10" is int)


# Test to check object instances using isinstance()
def test_is_instance():
    assert isinstance("hello hi", str)
    assert not isinstance("10", int)  # "10" is a string, not an int
    assert isinstance(5, int)  # 5 is an integer


# Test to check comparison operations (greater than, less than)
def test_gt_ls():
    assert 5 > 3
    assert 5 < 10


# Test list membership and logical operations
def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False, False]
    assert 1 in num_list
    assert 8 not in num_list
    assert all(num_list)
    assert not any(any_list)  # All are False, so any() returns False


# A simple Student class for testing object creation
class Student:
    def __init__(self, firstname: str, lastname: str, major: str, years: int):
        self.firstname = firstname
        self.lastname = lastname
        self.major = major
        self.years = years


# Unit test to verify that the Student object is initialized properly (without using a fixture)
def test_person_initialization_without_fixture():
    p = Student("John", "Doe", "CS", 3)

    assert p.firstname == "John", "firstname should be John"
    assert p.lastname == "Doe", "lastname should be John"
    assert p.major == "CS"
    assert p.years == 3


# Pytest fixture that returns a default Student instance
@pytest.fixture
def default_employee():
    return Student("John", "Doe", "CS", 3)


# Unit test using the fixture to test initialization
def test_person_initialization_with_fixture(default_employee):
    assert default_employee.firstname == "John", "firstname should be John"
    assert default_employee.lastname == "Doe", "lastname should be John"
    assert default_employee.major == "CS"
    assert default_employee.years == 3
