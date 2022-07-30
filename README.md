# distributed-content-sharing

## How to run

First start the bootstrap server. Please note that this code repository do not include code to the bootstrap server.


```bash
java BootstrapServer
```

Then start the python node.

```bash
python main.py -i 127.0.0.1 -I 172.19.208.1 -P 55555 --cli
```

Here,
* `-i` is the ip address that will be assigned to the starting node (local IP address).
* `-I` is the ip address of the bootstrap server.
* `-P` is the port number of the bootstrap server.
* `--cli` is the flag to enable the command line interface. If this flag is not provided, the user can't interact with the node. Node will just reply to the commands it receives.

There are some other arguments that can be used to control the node. All the arguments available in the system can be found like this.

```bash
python main.py -h
```

## How to intereact via cli

If the node was started with `--cli` flag, the user can interact with the node via the command line. The following commands are some of the assesntials.

| Command | Description |
|---------|-------------|
| quit | Automatically turn off the node gracefully. |
| print_peers | Print the list of peers nodes connected with this node. The node ID printed with this command can be used for other commands. |
| print_files | Print the list of files available in the node. |
| print_peers n | Send the print_peers command to the node ID n. |
| print_files n | Send the print_files command to the node ID n. |
| ? query | Send the search query to the network. |
| toggle_failed | Toggle the node to be failed. A failed node do not respond to the search queries. |
| download n filename | Get the download link for the file with the given name from the node with ID n. File name should be an exact match. |
| auto_search | Automatically search for files in the network by providing queries from `queries.txt` file, one after the other. |


All the available `cli` commands can be found in `cmd_server.py` file.

## About the files

| File name | Description |
|----------|-------------|
| cmd_server.py | The file that contains the command line interface. |
| file_server.py | The file that contains the file server which handle all files related processes. |
| files.txt | The file server will randomly pick file names from this file as the files available in the file server. |
| logger.py | The file that contains the logging service. |
| main.py | The file that contains the main function of the node. The entrypoint of the node. |
| node_server.py | When the node act as a server, this will be used for its processes. |
| node.py | When the node act as a client, this will be used for its processes. |
| queries.txt | When doing a `auto_search` cli command, search queries from this file will be used. |
| util.py | Utility functions. |

