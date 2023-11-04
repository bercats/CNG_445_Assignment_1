import sys
import re
import matplotlib.pyplot as plt


def parse_identities(identities_txt):
    try:
        identities_dict = {}
        file = open(identities_txt, "r")
        for line in file:
            if line.startswith("Commiter ID"):
                continue
            else:
                line_data = re.split(",", line)
                committer_id = line_data[0]
                name = line_data[1]
                email = line_data[2].strip()
                # Create a new person dictionary if the committer ID is not in the dictionary
                if committer_id not in identities_dict:
                    identities_dict[committer_id] = {
                        "name": name,
                        "email": email,
                    }
        return identities_dict
    except IOError:
        print("Could not open file " + identities_txt)
        return {}


def parse_commits(commit_txt, identities_dict):
    try:
        commit_dict = {}
        file = open(commit_txt, "r")
        for line in file:
            if line.startswith("Commit ID"):
                continue
            else:
                line_data = re.split(",", line)
                swm_tasks = [int(task) for task in line_data[1:4]]
                nfr_labeling = [int(label) for label in line_data[4:10]]
                soft_evol_tasks = [int(task) for task in line_data[10:14]]
                committer_id = line_data[14]
                # get person name from identities_dict
                name = identities_dict[committer_id]["name"]
                # Create a new commit dictionary if the name is not in the dictionary
                if name not in commit_dict:
                    commit_dict[name] = {
                        "SwM tasks": swm_tasks,
                        "NFR Labeling": nfr_labeling,
                        "SoftEvol tasks": soft_evol_tasks,
                    }
                else:
                    # add the tasks to the existing commit dictionary
                    for i in range(0, len(swm_tasks)):
                        commit_dict[name]["SwM tasks"][i] += int(swm_tasks[i])

                    for i in range(0, len(nfr_labeling)):
                        commit_dict[name]["NFR Labeling"][i] += int(nfr_labeling[i])

                    for i in range(0, len(soft_evol_tasks)):
                        commit_dict[name]["SoftEvol tasks"][i] += int(soft_evol_tasks[i])
        return commit_dict
    except IOError:
        print("Could not open file " + commit_txt)
        return

def plot_graph(title, labels, values):
    plt.bar(labels, values)
    plt.xlabel("Features")
    plt.ylabel("Number of commits")
    plt.title(title)
    plt.show()

def menu(commit_txt, identities_txt):
    id_dict = parse_identities(identities_txt)
    commit_dict = parse_commits(commit_txt, id_dict)
    choice = 0
    while choice != 4:
        print("\n --------------MENU--------------")
        print("1. Compare the number of commits done by a particular developer for a given classification scheme.")
        print("2. Compare the number of commits done by all developers, which are classified with a given feature.")
        print("3. Print the developer with the maximum number of commits for a given feature.")
        print("4. Exit")
        print("---------------------------------")
        print("Enter your choice: ")
        choice = int(input())
        if choice == 1:
            opt1(commit_dict)
            print("\n")
        elif choice == 2:
            opt2(commit_dict)
            print("\n")
        elif choice == 3:
            opt3(commit_dict)
            print("\n")
    return

def opt1(commit_dict):
    try:
        print("Select a developer: ")
        for name in commit_dict:
            print(name)
        name = input("Enter your choice: ")
        print("\n")
        print("Select a classification scheme: ")
        print("1. SwM tasks")
        print("2. NFR Labeling")
        print("3. SoftEvol tasks")
        scheme = int(input("Enter your choice: "))
        print("\n")
        if scheme == 1:
            labels = ["Adaptive", "Corrective", "Perfective"]
            values = [commit_dict[name]["SwM tasks"][0], commit_dict[name]["SwM tasks"][1],commit_dict[name]["SwM tasks"][2]]
            plot_graph(f"Comparison of {name}'s commits for SwM tasks", labels, values)
        elif scheme == 2:
            labels = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"]
            values = [commit_dict[name]["NFR Labeling"][0], commit_dict[name]["NFR Labeling"][1],
                      commit_dict[name]["NFR Labeling"][2], commit_dict[name]["NFR Labeling"][3],
                      commit_dict[name]["NFR Labeling"][4], commit_dict[name]["NFR Labeling"][5]]
            plot_graph(f"Comparison of {name}'s commits for NFR Labeling", labels, values)
        elif scheme == 3:
            labels = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]
            values = [commit_dict[name]["SoftEvol tasks"][0], commit_dict[name]["SoftEvol tasks"][1],
                      commit_dict[name]["SoftEvol tasks"][2], commit_dict[name]["SoftEvol tasks"][3]]
            plot_graph(f"Comparison of {name}'s commits for SoftEvol tasks", labels, values)
        else:
            print("Invalid choice.")
    except KeyError:
        print("Invalid name.")
    return


def opt2(commit_dict):
    try:
        print("Select a classification scheme:")
        print("1. SwM tasks")
        print("2. NFR Labeling")
        print("3. SoftEvol tasks")
        scheme = int(input("Enter your choice: "))
        print("\n")
        scheme_str = ""
        if scheme == 1:
            scheme_str = "SwM tasks"
            print("SwM tasks:")
            print("Select a feature:")
            feature = int(input("1. Adaptive Tasks\n2. Corrective Tasks\n3. Perfective Tasks\nEnter your choice: "))
            print("\n")
            feature_names = ["Adaptive Tasks", "Corrective Tasks", "Perfective Tasks"]
        elif scheme == 2:
            scheme_str = "NFR Labeling"
            print("NFR Labeling:")
            print("Select a feature:")
            feature = int(input("1. Maintainability\n2. Usability\n3. Functionality\n4. Reliability\n5. Efficiency\n6. Portability\nEnter your choice: "))
            print("\n")
            feature_names = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"]
        elif scheme == 3:
            scheme_str = "SoftEvol tasks"
            print("SoftEvol tasks:")
            print("Select a feature:")
            feature = int(input("1. Forward Engineering\n2. Re-Engineering\n3. Corrective Engineering\n4. Management\nEnter your choice: "))
            print("\n")
            feature_names = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]
        else:
            print("Invalid choice.")
            return

        if feature in range(1, len(feature_names) + 1):
            feature_name = feature_names[feature - 1]
            labels = []
            values = []
            for name in commit_dict:
                labels.append(name)
                values.append(commit_dict[name][scheme_str][feature - 1])
            plot_graph(f"Comparison of commits for {feature_name}", labels, values)
        else:
            print("Invalid choice.")

    except KeyError:
        print("Invalid name.")
    return

def opt3(commit_dict):
    try:
        print("Select a classification scheme: ")
        print("1. SwM tasks")
        print("2. NFR Labeling")
        print("3. SoftEvol tasks")
        scheme = int(input("Enter your choice: "))
        print("\n")
        scheme_str = ""
        if scheme == 1:
            scheme_str = "SwM tasks"
            print("SwM tasks:")
            print("Select a feature:")
            feature = int(input("1. Adaptive Tasks\n2. Corrective Tasks\n3. Perfective Tasks\nEnter your choice: "))
            print("\n")
            feature_names = ["Adaptive Tasks", "Corrective Tasks", "Perfective Tasks"]
        elif scheme == 2:
            scheme_str = "NFR Labeling"
            print("NFR Labeling:")
            print("Select a feature:")
            feature = int(input(
                "1. Maintainability\n2. Usability\n3. Functionality\n4. Reliability\n5. Efficiency\n6. Portability\nEnter your choice: "))
            print("\n")
            feature_names = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"]
        elif scheme == 3:
            scheme_str = "SoftEvol tasks"
            print("SoftEvol tasks:")
            print("Select a feature:")
            feature = int(input(
                "1. Forward Engineering\n2. Re-Engineering\n3. Corrective Engineering\n4. Management\nEnter your choice: "))
            print("\n")
            feature_names = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]
        else:
            print("Invalid choice.")
            return

        if feature in range(1, len(feature_names) + 1):
            feature_name = feature_names[feature - 1]
            max_commits = 0
            max_name = ""
            for name in commit_dict:
                if commit_dict[name][scheme_str][feature - 1] > max_commits:
                    max_commits = commit_dict[name][scheme_str][feature - 1]
                    max_name = name
            print(f"The developer with the maximum number of commits for {feature_name} is {max_name}: {max_commits}")
        else:
            print("Invalid choice.")
    except KeyError:
        print("Invalid name.")
    return


def main():
    if len(sys.argv) != 3:
        print("Usage: python commitanalyser.py commits.txt identities.txt")
        return
    print("Starting analysis...")
    commit_txt = sys.argv[1]
    identities_txt = sys.argv[2]
    menu(commit_txt, identities_txt)


if __name__ == '__main__':
    main()
