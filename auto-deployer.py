def main ():
    global args,args_dict
    args = parse_flags()
    args_dict = vars(args)

    ordered_args_list = get_args_by_order()

    hosts = load_hosts_yaml_file()

    host_objects = create_host_objects(hosts)
    
    run_all_commands(ordered_args_list,host_objects)
    
def parse_flags():
    """
    parse_flags parses input flags
    """
    import argparse
    parser = argparse.ArgumentParser(
        description='This script would help deployment of repeatedly tasks on remote machines for example run commands and send or receive files using ssh and scp respectively')
    
    #parser.add_argument('--host', nargs='+', help='added new host', dest='hosts',type=str, required=False)

    parser.add_argument('--command', dest='command',action='append', help="Run a command on all remote machines",required=True,type=str)
    parser.add_argument('--hosts', dest='hosts', help="Path of hosts YAML config file that contains ip's and passwords",required=True,type=str)
    parser.add_argument('--upload', dest='upload',action='append', help="Upload a file to a remote machine",required=False,type=str)
    parser.add_argument('--download', dest='download',action='append', help="Download a file from a remote machine",required=False,type=str)

    return parser.parse_args()

def get_args_by_order():
    import sys
    return [arg[2:] for arg in sys.argv if arg.startswith("--")]

def load_hosts_yaml_file():
    import yaml
    try:
        return load_yaml(args.hosts)
    except yaml.parser.ParserError as e:
        print(e)
        exit(1)

def load_yaml(yaml_file_path):
    import yaml
    with open(yaml_file_path, 'r') as cfg:
        return yaml.load(cfg)
        
def create_host_objects(hosts):
    host_objects = []
    for host in hosts:
        from host import HOST

        try:
            h = HOST(host["name"],host["ip"],host["user"],host["password"])
            host_objects.append(h)
        except KeyError as e:
            print(f"Error: maybe there is a problem is syntax of config file {args.hosts}: {e} does not exists in {host}")
        except Exception as e:
            print(e)
    return host_objects

def run_all_commands(ordered_args_list,host_objects):
    for arg in ordered_args_list:
        if isinstance(args_dict[arg],str):
            continue
        command = args_dict[arg].pop(0)
        # print(args_dict)
        for host in host_objects:
            try:
                output = host.run(arg,command)
            except Exception as e:
                print(e)
            else:
                if output is not "":
                    print (f'output of command \"{command}\" on {host.get_name()}:\n{output}')
                else:
                    print (f'command \"{command}\" ran on {host.get_name()}\n')
           
if __name__=="__main__":
    main()