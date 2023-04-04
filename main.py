import docker
import os
import subprocess


class FontColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Start
clients = docker.from_env()
containers = clients.containers.list(all=True)
while True:
    os.system('clear')
    # Print Main menu
    print(FontColors.OKGREEN + "1. List of all Containers" + FontColors.ENDC)
    print(FontColors.OKGREEN + "2. Start Container" + FontColors.ENDC)
    print(FontColors.OKGREEN + "3. Stop Container" + FontColors.ENDC)
    print(FontColors.OKGREEN + "4. Create new Container " + FontColors.ENDC)
    print(FontColors.FAIL + "5. Delete Container " + FontColors.ENDC)
    print(FontColors.OKGREEN + "6. Execute Container " + FontColors.ENDC)
    print(FontColors.OKGREEN + "7. Image Menu" + FontColors.ENDC)
    print(FontColors.WARNING + "q. exit" + FontColors.ENDC)
    user_select = input(":")
    if user_select == 'q':
        break

    # List of all containers
    if user_select == '1':
        os.system('clear')
        print(FontColors.BOLD + "List of all containers" + FontColors.ENDC)
        print(FontColors.HEADER + "Name \t\t Status" + FontColors.ENDC)
        for container in clients.containers.list(all=True, filters={"status": "running"}):
            print(container.name, '\t\t' + FontColors.OKGREEN + 'running' + FontColors.ENDC)
        for container in clients.containers.list(all=True, filters={"status": "exited"}):
            print(container.name, '\t\t' + FontColors.FAIL + 'exited' + FontColors.ENDC)
        input('Click Enter to continue')
        os.system('clear')

    # _________________________
    # Start Container
    if user_select == '2':
        os.system('clear')
        print(FontColors.BOLD + "Start Container" + FontColors.ENDC)
        idx = 0
        stopped_containers = []
        print(FontColors.HEADER + "# \tName \t\t Status" + FontColors.ENDC)
        for container in clients.containers.list(all=True, filters={"status": "exited"}):
            idx = idx + 1
            print(str(idx) + "\t" + container.name + '\t\texited')
            stopped_containers.append(container.short_id)
        UserContStart = input('Start Container #')
        try:
            short_id = (stopped_containers[int(UserContStart) - 1])
            print("Start Container name")
            # Start container using short ID
            container = clients.containers.get(short_id)
            print(short_id)
            container.start()
            input("Container Started " + FontColors.OKGREEN + "Successfully " + FontColors.ENDC)
        except ValueError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong back to main menu Error : 57001" + FontColors.ENDC)
        except IndexError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong" + FontColors.ENDC)

    # _________________________
    # Stop Container
    if user_select == '3':
        os.system('clear')
        print(FontColors.BOLD + "Stop Container" + FontColors.ENDC)
        idx = 0
        started_containers = []
        print(FontColors.HEADER + "# \tName \t\t Status" + FontColors.ENDC)
        for container in clients.containers.list(all=True, filters={"status": "running"}):
            idx = idx + 1
            print(str(idx) + "\t" + container.name + '\t\trunning')
            started_containers.append(container.short_id)
        UserContStop = input('Stopp Container #')
        try:
            short_id = (started_containers[int(UserContStop) - 1])
            print("Stop Container name")
            # Start container using short ID
            container = clients.containers.get(short_id)
            container.stop()
            input("Container stopped " + FontColors.OKGREEN + "Successfully " + FontColors.ENDC)
        except ValueError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong back to main menu Error : 57002" + FontColors.ENDC)
        except IndexError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong" + FontColors.ENDC)

    # _________________________
    # Create New Container
    if user_select == '4':
        os.system('clear')
        images = clients.images.list()
        # Step 1: List all available images
        print(FontColors.OKGREEN + "Available images: " + FontColors.ENDC)
        for i, image in enumerate(images):
            print(f"{i + 1}- {image.tags[0]}")
        try:
            # Step 2: User chooses an image
            image_num = int(input(FontColors.OKGREEN + "Choose an image number: " + FontColors.ENDC))
            image_tag = images[image_num - 1].tags[0]
            os.system('clear')
            print(FontColors.OKGREEN + "Image:" + FontColors.ENDC + str(image_tag))
        except ValueError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong back to main menu Error : 57001" + FontColors.ENDC)
            continue
        except IndexError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong" + FontColors.ENDC)
            continue
        # Step 3: Ask for container name
        container_name = input(FontColors.OKGREEN + 'Container Name:' + FontColors.ENDC)
        os.system('clear')
        print(FontColors.OKGREEN + "Image:" + FontColors.ENDC + image_tag)
        print(FontColors.OKGREEN + "Container Name:" + FontColors.ENDC + container_name)
        # Step 4: Ask for port forwarding
        port_forwarding = input(FontColors.OKGREEN + "Port forwarding (Yes/No): " + FontColors.ENDC).lower() == "yes"
        if port_forwarding:
            # Ask for ports to forward
            host_port = input(FontColors.OKGREEN + "\tHost port: " + FontColors.ENDC)
            container_port = input(FontColors.OKGREEN + "\tContainer port: " + FontColors.ENDC)
            ports = {int(host_port): int(container_port)}
        else:
            ports = None
        # Step 5: Ask for volume creation
        volume_creation = input(FontColors.OKGREEN + "Volume creation (Yes/No): " + FontColors.ENDC).lower() == "yes"
        if volume_creation:
            # Ask for volume name
            host_volume = input(FontColors.OKGREEN + "\tHost volume: " + FontColors.ENDC)
            container_volume = input(FontColors.OKGREEN + "\tContainer volume: " + FontColors.ENDC)
            volumes = {host_volume: {'bind': container_volume, 'mode': 'rw'}}
        else:
            volumes = None
        # Step 6: Ask for container label
        os.system('clear')
        # Step 7: Print all setup and ask for confirmation
        print(FontColors.OKGREEN + "Selected image:" + FontColors.ENDC + image_tag)
        print(FontColors.OKGREEN + "Container name:" + FontColors.ENDC + container_name)
        print(FontColors.OKGREEN + "Port forwarding:" + FontColors.ENDC + str(ports))
        print(FontColors.OKGREEN + "Volume creation:" + FontColors.ENDC + str(volumes))

        confirm = input(FontColors.OKGREEN + "Do you confirm this setup? (Yes/No): " + FontColors.ENDC).lower() == "yes"
        if confirm:
            # Create container
            container = clients.containers.run(
                image_tag,
                detach=True,
                tty=True,
                name=container_name,
                ports=ports,
                volumes=volumes
            )
            container.start()
            print(container.id)
            print(volumes)

            input(f"Container {container.name} has been created.")
        else:
            print("Setup canceled.")

    # _________________________
    # Delete Container remove
    if user_select == '5':
        os.system('clear')
        print(FontColors.FAIL + "Delete Container" + FontColors.ENDC)
        idx = 0
        started_containers = []
        print(FontColors.HEADER + "# \tName \t\t Status" + FontColors.ENDC)
        for container in clients.containers.list(all=True, filters={"status": "exited"}):
            idx = idx + 1
            print(str(idx) + "\t" + container.name + '\t\trunning')
            started_containers.append(container.short_id)
        UserContStop = input('Stopp Container #')
        try:
            short_id = (started_containers[int(UserContStop) - 1])
            print("Delete Container name")
            # Start container using short ID
            container = clients.containers.get(short_id)
            container.remove()
            input("Container Delete " + FontColors.OKGREEN + "Successfully " + FontColors.ENDC)
        except ValueError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong back to main menu Error : 57002" + FontColors.ENDC)
        except IndexError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong" + FontColors.ENDC)

    # _________________________
    # Execute Container
    if user_select == '6':
        os.system('clear')
        print(FontColors.BOLD + "Execute Container" + FontColors.ENDC)
        idx = 0
        started_containers = []
        print(FontColors.HEADER + " \t Name \t\t Status" + FontColors.ENDC)
        for container in clients.containers.list(all=True, filters={"status": "running"}):
            idx = idx + 1
            print("#" + str(idx) + "\t" + container.name + '\t'+FontColors.OKGREEN + 'running'+FontColors.ENDC)
            started_containers.append(container.short_id)
        UserContStop = input('Stopp Container #')
        try:
            short_id = (started_containers[int(UserContStop) - 1])
            print("Execute Container name" + short_id)
            # Start container using short ID
            container = clients.containers.get(short_id)
            terminal = 'docker container list -a'
            proc = subprocess.Popen([terminal], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            outline = ''.join(map(chr, out))
            phrase_to_list = (outline.splitlines())
            line_o = []
            SHORTID = IMAGE = COMMAND = None

            for line_t in phrase_to_list:
                line_t = line_t.replace('/t', '#').split()
                line_o.append(line_t)
            for txt in line_o:
                if short_id == txt[0]:
                    SHORTID = txt[0]
                    IMAGE = txt[1]
                    COMMAND = txt[2]
            code = "docker exec -it " + SHORTID+" " + COMMAND
            print(IMAGE + ':' + code)
            os.system(code)
            input("Container Exit " + FontColors.OKGREEN + "Successfully " + FontColors.ENDC)
        except ValueError:
            os.system('clear')
            input(FontColors.FAIL + "Something wrong back to main menu Error : 57002" + FontColors.ENDC)

    # _________________________
    # Image Menu
    if user_select == '7':
        os.system('clear')
        images = clients.images.list()
        # Print Image Menu
        print(FontColors.OKGREEN + "1. Available image/s" + FontColors.ENDC)
        print(FontColors.OKGREEN + "2. Download new image" + FontColors.ENDC)
        print(FontColors.FAIL + "3. Delete image" + FontColors.ENDC)
        i_selection = input(FontColors.OKGREEN + ":" + FontColors.ENDC)
        if i_selection == '1':
            print(FontColors.OKGREEN + "Available images: " + FontColors.ENDC)
            for i, image in enumerate(images):
                print(f"{i + 1}- {image.tags[0]}")
            input(FontColors.OKGREEN + "." + FontColors.ENDC)
        # Download Image
        if i_selection == '2':
            os.system('clear')
            images = clients.images.list()
            image_tag = input(FontColors.OKGREEN + "Choose an image download: " + FontColors.ENDC)
            try:
                clients.images.pull(image_tag)
                print(FontColors.OKGREEN + f"Successfully downloaded {image_tag}." + FontColors.ENDC)
                input(FontColors.OKGREEN + "." + FontColors.ENDC)
            except docker.errors.ImageNotFound:
                input(FontColors.FAIL + f"Error: {image_tag} not found on Docker Hub." + FontColors.ENDC)
            except docker.errors.APIError:
                input(FontColors.FAIL + f"Error: Failed to download {image_tag}." + FontColors.ENDC)
        # Delete Image
        if i_selection == '3':
            os.system('clear')
            images = clients.images.list()
            print(FontColors.OKGREEN + "Available images: " + FontColors.ENDC)
            for i, image in enumerate(images):
                print(f"{i + 1}- {image.tags[0]}")
            image_num = input(FontColors.FAIL + "Choose an image to DELETE: " + FontColors.ENDC)
            try:
                image_tag = images[int(image_num) - 1].tags[0]
            except ValueError or TypeError:
                os.system('clear')
                input(FontColors.FAIL + "Something wrong back to main menu Error : 57002" + FontColors.ENDC)
                continue
            except IndexError:
                os.system('clear')
                input(FontColors.FAIL + "Something wrong" + FontColors.ENDC)
                continue
            try:
                clients.images.remove(image_tag)
                print(FontColors.OKGREEN + f"Successfully Delete {image_tag}." + FontColors.ENDC)
                input(FontColors.OKGREEN + "." + FontColors.ENDC)
            except docker.errors.ImageNotFound:
                print(FontColors.FAIL + f"Error: {image_tag} not found on Docker Hub." + FontColors.ENDC)
                input(FontColors.FAIL + "Image Not Found" + FontColors.ENDC)
                continue
            except docker.errors.APIError:
                print(FontColors.FAIL + f"Error: Failed to Delete {image_tag}." + FontColors.ENDC)
                input(FontColors.FAIL + "APIError" + FontColors.ENDC)
                continue
