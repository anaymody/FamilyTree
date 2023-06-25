# NAME: Anay Mody
# ID: 8649820623
# DATE: 2023-05-04
# DESCRIPTION: Similar to the friend connections networks and a few of the last couple of projects,
# this project aims to allow users to create and interact with a family tree. Each member of
# the family tree will have unique characteristics, including name, birthdate, and a
# description of who they are. Some of these characteristics will be required, such as the
# name, while others can be optional. Each member will also have connections to other
# members of the family tree. This project will be restricted to having lists of siblings,
# parents, grandparents, uncles/aunts, and cousins. Cases such as divorces, step-siblings,
# half-siblings will not be taken into account. In addition, each name must be
# unique. The user of the program will also be able to modify the family tree by adding
# parents or children, or finding the relation between two people. After any changes
# have been made, a file will be outputted to the user which can then be inputted the
# next time they want to add data or analyze a specific family tree. This family tree will also
# follow the lineage of one member, meaning that there is one member at the top, and all their
# children, and their children's children, etc. will be the only members that will be considered
# to be blood related. Spouses and others will not be able to have other family members attached
# to them, other than their respective spouses and children.

from typing import IO, Tuple

# Representations of menu options
ADD_CONNECTION = "1"
VIEW_MEMBERS = "2"
MEMBER_INFO = "3"
FIND_RELATION = "4"
MODIFY = "5"
SAVE = "6"

# Global dictionary to be accessed through all functions and classes
family_list = {}


def add_birthday(member):
    """This function creates adds a birthday for the member it is called for

    """
    month = input("Enter month (0-12): ")
    if month == "?":
        print("Skipping...")
        return ""
    if not month.isdigit() or int(month) < 0 or int(month) > 12:
        print("Invalid input. Exiting")
        return ""
    else:
        day = input("Enter day (0-31): ")
        if not day.isdigit() or int(day) < 0 or int(day) > 31:
            print("Invalid input. Exiting")
            return ""
        else:
            year = input("Enter year: ")
            if not year.isdigit():
                print("Invalid input. Exiting")
                return ""

    member.birthday = month + "/" + day + "/" + year


class TreeMember:
    def __init__(self, name="", top_of_tree=False, birthday="",
                 description="", spouse="", children_list=None, tree_parent=""):
        """This function initializes class attributes to either default values or passed values
        upon instantiation of the TreeMember object

        """
        if children_list is None:
            children_list = []
        if len(children_list) != 0:
            if children_list[0] == "":
                children_list = []
        if name == "":
            self.name = input("What is this person's full name: ").title().strip()
        else:
            self.name = name
        self.birthday = birthday
        self.description = description
        self.spouse = spouse
        self.tree_parent = tree_parent
        self.parents_list = []
        self.children_list = children_list
        self.top_of_tree = top_of_tree

    def __str__(self):
        """This function shows how the object should be represented as a string

        """
        return self.name

    def add_parent(self, parent_name: str, is_tree_parent: bool):
        """This function checks if someone has two parents, and if not, adds
        them to the parents_list. If the parent is in their lineage, or is_tree_parent
        is true, it makes them the tree parent

        """
        if len(self.parents_list) >= 2:
            print("This person already has 2 parents.")
        else:
            if self.tree_parent == "" and is_tree_parent:
                self.tree_parent = parent_name
                self.top_of_tree = False
                family_list[parent_name].top_of_tree = True
            self.parents_list.append(parent_name)

    def add_child(self, child_name):
        """Adds child_name to TreeMember's children_list

        """
        self.children_list.append(child_name)

    def member_info(self):
        """Displays the information about the attributes of a TreeMember

        """
        print("Name:\n\t" + self.name + "\n\nBirthday:\n\t" + self.birthday + "\n\nDescription:\n\t" + self.description)
        print("\nSpouse:\n\t" + self.spouse)
        print("\nParents: ")
        if len(self.parents_list) == 0:
            print("\tThere are no parents added")
        for parent in self.parents_list:
            print("\t" + parent)
        print("\nChildren: ")
        if len(self.children_list) == 0:
            print("\tThere are no children added")
        for child in self.children_list:
            print("\t" + str(child))

    def __repr__(self):
        """This is how the TreeMember class is represented if typed into
        the Python Console

        """
        return self.name


class NonTreeMember:
    def __init__(self, spouse, name="", birthday="",
                 description="", children_list=None):
        """This function initializes class attributes to either default values or passed values
                upon instantiation of the NonTreeMember object

        """
        if children_list is None:
            children_list = []
        if name == "":
            self.name = input("What is this person's full name: ").title().strip()
        else:
            self.name = name
        self.birthday = birthday
        self.description = description
        self.spouse = spouse
        self.children_list = children_list
        self.children_list = family_list[self.spouse].children_list

    def add_child(self, child_name):
        """Adds child_name to TreeMember's children_list

        """
        self.children_list.append(child_name)

    def member_info(self):
        """Displays the information about the attributes of a TreeMember

        """
        print("Name:\n\t" + self.name + "\n\nBirthday:\n\t" + self.birthday + "\n\nDescription:\n\t" + self.description)
        print("\nSpouse:\n\t" + self.spouse)
        print("\nChildren: ")
        if len(self.children_list) == 0:
            print("\tThere are no children added")
        for child in self.children_list:
            print("\t" + child)


def open_file() -> Tuple[IO, str]:
    """This function opens the profile file or connection file passed by the user
    when file_type is passed as either one of those options. It also uses exceptions
    to make sure that the file can open properly, and if so, returns a file_pointer.

    """
    file_pointer = None
    while file_pointer is None:
        file_name = input("Enter the input filename:\n")
        try:
            file_pointer = open(file_name, 'r')
        except IOError:
            print(f"An error occurred while opening the file {file_name}.\n"
                  f"Make sure the file path and name are correct \nand that "
                  f"the file exist and is readable.")

    return file_pointer, file_name


def read_file(fp) -> None:
    """This function takes the fp passed to it and parses it using special instructions. It reads
    each line, skipping the format line, and reads the information into a list, member_info. Each
    index corresponds to a specific attribute, and after each of these attributes is stripped, a
    new object is created, either TreeMember or NonTreeMember based on what is specified in the
    file. This function also adds children to each parent since the file does not contain that
    information. Each instantiated member is added to family_list

    """
    fp.readline()
    for line in fp:
        member_info = line.strip().split("|")
        name = member_info[1].strip()
        birthday = member_info[2].strip()
        description = member_info[3].strip()
        spouse = member_info[4].strip()
        # Converts a string representation of a list to a real Python list
        children_list = member_info[5].strip().strip("[]").strip("'").split(",")
        # For loop strips any remaining apostrophes from each child in children_list
        for i in range(len(children_list)):
            children_list[i] = children_list[i].strip().strip("'")
        if member_info[0] == "TM":
            # Additional two attributes only included in TreeMembers
            top_of_tree = member_info[6].strip()
            if top_of_tree == "False":
                top_of_tree = False
            else:
                top_of_tree = True
            tree_parent = member_info[7].strip()
            family_list[name] = TreeMember(name, top_of_tree, birthday, description, spouse, children_list, tree_parent)
        else:
            family_list[name] = NonTreeMember(spouse, name, birthday, description, children_list)
    fp.close()

    for member in family_list:
        for child in family_list[member].children_list:
            if child != "":
                family_list[child].parents_list.append(member)


def receive_verify_member_name(member_name: str, in_family=True) -> str:
    valid = False
    # in_family checks whether function calling receive_verify_member_name is looking for a member, or adding a new one
    if in_family:
        # Asks user to input names until a name is found in family_list
        while not valid:
            if member_name in family_list.keys():
                valid = True
            elif member_name == "?":
                return member_name
            else:
                member_name = input("This person doesn't exist yet! Please try again (? to quit): ").title().strip()
    # Case where user is looking to add a new member
    else:
        # Keeps asking user to input a name until that name is not in the family
        while not valid:
            if member_name not in family_list.keys():
                valid = True
            elif member_name == "?":
                return member_name
            else:
                member_name = input("This person already exists! Please try again (? to quit): ").title().strip()

    return member_name.title().strip()


def add_relation():
    """This function adds a parent, child, or spouse relation to a TreeMember. This connection can be
    either a TreeMember or NonTreeMember, but they must have a unique name.

    """
    member_name = input("Please enter the name of the member you would like to add a connection to: ").title().strip()
    member_name = receive_verify_member_name(member_name)
    if member_name == "?":
        print("Exiting...")
        return

    # Makes sure that the connection is only being added to TreeMembers
    if type(family_list[member_name]) == NonTreeMember:
        print("You can only add connections to members that are in this tree's lineage.")
        return

    # Asks for the name of the new user
    connection_name = input("Please enter the name of the new member: ").title().strip()
    connection_name = receive_verify_member_name(connection_name, False)
    if member_name == "?":
        print("Exiting...")
        return

    # Checks which relation should be added
    relation_type = input("Is " + connection_name + " " + member_name + "'s parent, child, or spouse? ").lower().strip()

    # Verifies user input
    while relation_type not in ["parent", "child", "spouse", "?"]:
        relation_type = input("Invalid relation. Try again. To exit, enter '?': ").lower().strip()

    if relation_type == "parent":
        # Makes sure that the member does not have 2 parents already
        if len(family_list[member_name].parents_list) >= 2:
            print("Error. " + member_name + " already has two parents. " +
                  connection_name + " cannot be added to the tree.")
            return
        # Asks whether the new user should be a TreeMember
        user_choice = input("Is this person's lineage in the tree? (y/n): ")
        is_tree_parent = True
        # Case for NonTreeMember parent
        if user_choice.lower() == "n":
            is_tree_parent = False
            # Ensures that the first parent added is a TreeMember (useful for file saving and parsing)
            if family_list[member_name].tree_parent == "":
                tree_parent_name = input("Please enter the spouse of " + connection_name + ": ").title().strip()
                tree_parent_name = receive_verify_member_name(tree_parent_name, False)
                if member_name == "?":
                    print("Exiting...")
                    return
                family_list[tree_parent_name] = TreeMember(tree_parent_name)
                # Adds NonTreeMember parent to TreeMember parent spouse
                family_list[tree_parent_name].spouse = connection_name
                print(tree_parent_name + " has been added to the family tree!")

                # Adds NonTreeMember parent to family_list
                family_list[member_name].add_parent(tree_parent_name, True)
                family_list[connection_name] = NonTreeMember(tree_parent_name, connection_name)
            # In case TreeMember parent already added
            else:
                # Creates NonTreeMember and adds existing spouse
                family_list[connection_name] = NonTreeMember(family_list[member_name].tree_parent, connection_name)
                family_list[family_list[member_name].tree_parent].spouse = connection_name

        # Case for TreeMember lineage
        else:
            # Makes sure there isn't already a tree_parent
            if family_list[member_name].tree_parent != "":
                print(member_name + " already has a parent in the tree's lineage. " + connection_name +
                      " cannot be added to the tree.")
                return
            # Adds new TreeMember to family_list
            family_list[connection_name] = TreeMember(connection_name)

        # Creates a parent/child relation
        family_list[member_name].add_parent(connection_name, is_tree_parent)
        family_list[connection_name].add_child(member_name)

    # Creates a child/parent relationship and adds the parent as the child's tree_parent since both are TreeMembers
    elif relation_type == "child":
        family_list[connection_name] = TreeMember(connection_name)
        family_list[connection_name].add_parent(member_name, True)
        family_list[member_name].add_child(connection_name)
        family_list[connection_name].tree_parent = member_name

    elif relation_type == "spouse":
        # Makes sure that member_name does not already have a spouse
        if family_list[member_name].spouse == "":
            # Creates a NonTreeMember and adds this person as a parent for all children of TreeMember
            family_list[connection_name] = NonTreeMember(member_name, connection_name)
            family_list[member_name].spouse = connection_name
            for child in family_list[member_name].children_list:
                family_list[child].add_parent(connection_name, False)
        else:
            print(member_name + " already has a spouse! Cannot add " + connection_name + " to the tree.")
            return
    # Case where user wants to exit
    else:
        print("Exiting...")
        return
    # Prints if there is a success
    print(connection_name + " has been added to the family tree!")


def find_relation(m1_name, m2_name) -> str:
    """Calculates the relation between two different members in the tree. Only calculates the
    relation with NonTreeMembers if it is a parent/child or spousal relation. Uses an algorithm
    and if statements to figure out what type of relation exists (siblings, niece/nephew, uncle/aunt,
    grandparent/grandchild, and the great- equivalents that exist)

    """
    # Establishes object versions of the member names passed to find_relation
    m1 = family_list[m1_name]
    m2 = family_list[m2_name]

    # Self relation
    if m1_name == m2_name:
        return m1_name + " is " + m2_name

    # Parent/child relation
    if m2_name in m1.children_list:
        return m1_name + " is the parent of " + m2_name
    elif m1_name in m2.children_list:
        return m1_name + " is the child of " + m2_name

    # Spousal relation
    if m1.spouse == m2_name:
        return m1_name + " is the spouse of " + m2_name

    # From this point onwards, only TreeMembers can have relations found
    if type(m1) == NonTreeMember:
        return m1_name + " is not in the lineage of the tree"
    if type(m2) == NonTreeMember:
        return m2_name + " is not in the lineage of the tree"

    # Creates a list finding the lineage of each
    m1_lineage = [m1_name]
    m2_lineage = [m2_name]

    # Lineage list added to include all people leading directly up to the person who is at the top of the tree
    tree_member = m1
    while tree_member.tree_parent != "":
        m1_lineage.append(tree_member.tree_parent)
        tree_member = family_list[tree_member.tree_parent]

    tree_member = m2
    while tree_member.tree_parent != "":
        m2_lineage.append(tree_member.tree_parent)
        tree_member = family_list[tree_member.tree_parent]

    # Determines the leas_common_member in the lineage of each to determine how closely related the members are
    least_common_member = ""
    for member in m1_lineage:
        if member in m2_lineage:
            least_common_member = member
            break
    # Assigns the location of the least_common_member as the index
    m1_index = m1_lineage.index(least_common_member)
    m2_index = m2_lineage.index(least_common_member)

    # Closest relation is in lineage, implying grandparent/grandchild (includes great- if necessary)
    if m1_index == 0:
        # Used to calculate if great- prefix is necessary, and if so, how many
        relation = "great-" * (m2_index - 2)
        return m1_name + " is the " + relation + "grandparent of " + m2_name
    if m2_index == 0:
        relation = "great-" * (m1_index - 2)
        return m1_name + " is the " + relation + "grandchild of " + m2_name

    # The closest relative is one level up, implying that these are either siblings, nieces/nephews, or uncles/aunts
    if m1_index == 1:
        # If both indices one level up, they are siblings
        if m2_index == 1:
            return m1_name + " is the sibling of " + m2_name
        # Two levels implies uncle/aunt
        if m2_index == 2:
            return m1_name + " is the uncle/aunt of " + m2_name

        # Implies grandaunt/granduncle, including great- prefix if necessary, with similar index calculation
        relation = "great-" * (m2_index - 3)
        return m1_name + " is the " + relation + "granduncle/grandaunt of " + m2_name
    # Same as above, with opposite relations
    if m2_index == 1:
        if m1_index == 2:
            return m1_name + " is the niece/nephew of " + m2_name
        relation = "great-" * (m1_index - 3)
        return m1_name + " is the " + relation + "grandniece/grandnephew of " + m2_name

    # If no relations applied yet, smaller index corresponds to type of cousin
    type_of_cousin = str(min(m1_index, m2_index) - 1)
    suffix = "th"
    if int(type_of_cousin) != 11 and int(type_of_cousin) % 10 == 1:
        suffix = "st"
    elif int(type_of_cousin) != 12 and int(type_of_cousin) % 10 == 2:
        suffix = "nd"
    elif int(type_of_cousin) != 13 and int(type_of_cousin) % 10 == 3:
        suffix = "rd"
    # Difference in indices corresponds to generational removal
    removal = str(abs(m1_index - m2_index))

    if removal == "0":
        # Return statement if same generation
        return m1_name + " is the " + type_of_cousin + suffix + " cousin of " + m2_name
    else:
        # Return statement if there is generational difference
        return m1_name + " is the " + type_of_cousin + suffix + " cousin " + removal + " times removed of " + m2_name


def modify_member(member_name: str) -> None:
    """Allows the user to change certain attributes of member_name, like the birthday, and description

    """
    member = family_list[member_name]
    print("Enter the birthday (? to skip)")
    add_birthday(member)
    member.description = input("Please enter a short description (? to skip): ").strip()
    if member.description == "?":
        print("Skipping...")
        member.description = ""
    print(member_name + " has been modified!")


def display_menu() -> str:
    """This function creates a menu that is reused is select_action, and displays
    the options a user can take when they are running the program.

    """
    print("\nPlease select one of the following options.\n")
    print(ADD_CONNECTION + ". Add a family member to the tree\n" +
          VIEW_MEMBERS + ". See all of the members in the tree\n" +
          MEMBER_INFO + ". See information about a specific member\n" +
          FIND_RELATION + ". See the relation between two members in the tree\n" +
          MODIFY + ". Change the corresponding attributes of a member\n" +
          SAVE + ". Save changes and exit\n"
          )

    return input("Enter your choice here.\n")


def select_action(input_file_present: bool, input_file_name: str) -> str:
    """This function asks the user which action they would like to take, and the
    actions are specified by the display_menu() function. Once an action is selected,
    this function calls the appropriate corresponding function and takes the next action.
    The actions allowed are: add connection, show members in the tree, show info about a
    member, find the relation between two members in the tree, change the attributes of
    members, and save modified information to a new file.

    """
    response = display_menu()
    valid = False
    # Repeats until a valid response is given
    while not valid:
        if response in [ADD_CONNECTION, VIEW_MEMBERS, MEMBER_INFO, FIND_RELATION, MODIFY, SAVE]:
            valid = True
        if response == ADD_CONNECTION:
            add_relation()
        elif response == VIEW_MEMBERS:
            for member in family_list:
                print(member)
        elif response == MEMBER_INFO:
            member_name = input("Which member would you like to know about: ").title().strip()
            member_name = receive_verify_member_name(member_name)
            if member_name == "?":
                print("Exiting...")
                return "Continue"
            family_list[member_name].member_info()
        elif response == FIND_RELATION:
            member1_name = input("Please enter the name of the first member: ").title().strip()
            member1_name = receive_verify_member_name(member1_name)
            if member1_name == "?":
                print("Exiting...")
                return "Continue"
            member2_name = input("Please enter the name of the second member: ").title().strip()
            member2_name = receive_verify_member_name(member2_name)
            if member2_name == "?":
                print("Exiting...")
                return "Continue"
            relation = find_relation(member1_name, member2_name)
            print(relation)

        elif response == MODIFY:
            member_name = input("Which member would you like to modify? ").title().strip()
            member_name = receive_verify_member_name(member_name)
            if member_name == "?":
                print("Exiting...")
                return "Continue"
            modify_member(member_name)
        elif response == SAVE:
            save_changes(input_file_present, input_file_name)
            return "Exit"
        else:
            input("Invalid input. Hit enter to try again: ")
            response = display_menu()

    input("\nPress enter to continue.")

    return "Continue"


def initialization() -> Tuple[bool, str]:
    """This function initially calls checks if the user has an existing family tree file. If yes,
    it calls the open_file function to get the family tree information. If not, it asks the user
    to start building the tree with an initial member. It keeps track of which option was chosen
    and returns the input_file_present bool and file_name.

    """
    user_choice = input("Do you have an existing file you would like to modify? (y/n): ")
    while user_choice.lower() not in ("n", "y"):
        print("Invalid input\n")
        user_choice = input("Do you have an existing file you would like to modify? (y/n): ")
    if user_choice.lower() == "n":
        input_file_present = False
    else:
        input_file_present = True

    input_file_name = ""
    if input_file_present:
        fp, input_file_name = open_file()
        read_file(fp)
    else:
        first_member = input("Please enter a starting member to build your family tree: ").title().strip()
        family_list[first_member] = TreeMember(first_member, True)
        print(first_member + " has been added to the family tree!")

    return input_file_present, input_file_name


def save_changes(file_present: bool, file_name: str) -> None:
    """This function prompts the user to input a new file name to save
    their modified data to if the tree they have created is new. If not, it
    saves the information to the file that is passed, and passes back a file
    containing a copy of the original data. It then writes the updated information in the
    same format as an input file.

    """
    # If a file was passed, copies the original contents to a new file with the same name, but _orig added to the end
    if file_present:
        input_fp = open(file_name, "r")
        orig_file = file_name.replace(".txt", "_orig.txt")
        orig_fp = open(orig_file, "w")

        for line in input_fp:
            orig_fp.write(line)

        orig_fp.close()
        input_fp.close()

    # Case if the family tree is brand new. Asks user to give a filename where they would like to save the information
    else:
        # Requires .txt ending
        while ".txt" not in file_name:
            file_name = input("Please enter a file name ending with .txt: ")

    # Creates a file pointer that points at file_name for writing
    output_fp = open(file_name, "w")
    # Information about data that follows in each line, separated by "|" character
    output_fp.write("class_type|name|birthday|description|spouse|children_list|top_of_tree|tree_parent\n")

    # Each line has data for each family member
    for member in family_list:
        member = family_list[member]

        # Writes corresponding code for TreeMember or NonTreeMember
        if type(member) == TreeMember:
            output_fp.write("TM|")
        else:
            output_fp.write("NTM|")

        # Common attributes between TM and NTM
        output_fp.write(member.name + "|" +
                        member.birthday + "|" +
                        member.description + "|" +
                        member.spouse + "|" +
                        str(member.children_list))

        # Additional two attributes for TMs
        if type(member) == TreeMember:
            output_fp.write("|" + str(member.top_of_tree) + "|" + member.tree_parent)

        output_fp.write("\n")

    input("All changes saved in " + file_name + " Hit enter to exit.")


def main():
    print("Welcome to Family Tree Maker!")
    input_file_present, input_file_name = initialization()

    action = "Continue"
    while action != "Exit":
        action = select_action(input_file_present, input_file_name)

    input("Thank you for using Family Tree Maker!")


if __name__ == "__main__":
    main()
