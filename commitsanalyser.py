import sys
import matplotlib.pyplot as plt

swmFeatures = ["Adaptive", "Corrective", "Perfective"]
nfrFeatures = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"]
softEvolFeatures = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]
classificationSchemes = ["SwM tasks", "NFR Labeling", "SoftEvol tasks"]

def parse_identities(identities_txt):
    identities_dict = {}
    try:
        file = open(identities_txt, "r")
        lines = file.readlines()
        for line in lines[1:]:
            line_data = line.split(",")
            committer_id = line_data[0]
            name = line_data[1]
            email = line_data[2].strip()
            # Create a new person dictionary if the committer ID is not in the dictionary
            identities_dict[committer_id] = {"name": name, "email": email}
        return identities_dict
    except IOError:
        print("Could not open file " + identities_txt)
        return {}
    finally:
        file.close()

def parse_commits(commit_txt, identities_dict):
    commit_dict = {}
    try:
        file = open(commit_txt, "r")
        lines = file.readlines()
        for line in lines[1:]:
            line_data = line.split(",")
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
    finally:
        file.close()

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
            combined_opt(commit_dict, choice)
            print("\n")
        elif choice == 3:
            combined_opt(commit_dict, choice)
            print("\n")
    return


def opt1(commit_dict):
    names = list(commit_dict.keys())
    labels = None
    try:
        print("Select a developer: ")
        for i, name in enumerate(commit_dict, 1):
            print(f"{i}. {name}")
        name = names[int(input("Enter your choice: ")) - 1]
        print("\n")
        print("Select a classification scheme:")
        for i, scheme in enumerate(classificationSchemes, 1):
            print(f"{i}. {scheme}")
        scheme = int(input("Enter your choice: "))
        print("\n")
        if scheme == 1:
            labels = swmFeatures
        elif scheme == 2:
            labels = nfrFeatures
        elif scheme == 3:
            labels = softEvolFeatures
        else:
            print("Invalid choice.")
        values = commit_dict[name][classificationSchemes[scheme - 1]]
        plot_graph(f"Comparison of {name}'s commits for {classificationSchemes[scheme - 1]}", labels, values)
    except KeyError:
        print("Invalid name.")
    return

def combined_opt(commit_dict, option):
    try:
        print("Select a classification scheme:")
        for i, scheme in enumerate(classificationSchemes, 1):
            print(f"{i}. {scheme}")
        scheme = int(input("Enter your choice: "))
        print("\n")
        if scheme == 1:
            feature_names = swmFeatures
        elif scheme == 2:
            feature_names = nfrFeatures
        elif scheme == 3:
            feature_names = softEvolFeatures
        else:
            print("Invalid choice.")
            return

        print("Select a feature:")
        for i, feature in enumerate(feature_names, 1):
            print(f"{i}. {feature}")
        feature = int(input("Enter your choice: "))
        print("\n")

        if feature in range(1, len(feature_names) + 1):
            feature_name = feature_names[feature - 1]

            if option == 2:
                labels = list(commit_dict.keys())
                values = []
                for name in commit_dict:
                    values.append(commit_dict[name][classificationSchemes[scheme - 1]][feature - 1])
                plot_graph(f"Comparison of commits for {feature_name}", labels, values)

            elif option == 3:
                max_commits = 0
                max_developer = ""
                for name in commit_dict:
                    if commit_dict[name][classificationSchemes[scheme - 1]][feature - 1] > max_commits:
                        max_commits = commit_dict[name][classificationSchemes[scheme - 1]][feature - 1]
                        max_developer = name
                print(f"{max_developer} has {max_commits} commits classified by {feature_name}")
            else:
                print("Invalid option.")
        else:
            print("Invalid choice.")
    except KeyError:
        print("Invalid name.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python commitsanalyser.py commits.txt identities.txt")
        return
    print("Starting analysis...")
    commit_txt = sys.argv[1]
    identities_txt = sys.argv[2]
    menu(commit_txt, identities_txt)

if __name__ == '__main__':
    main()
