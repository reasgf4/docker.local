import docker
import os
import platform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_docker_connection_methods():
    """Test multiple Docker connection methods to find one that works"""
    
    print(f"Platform: {platform.system()}")
    print(f"Python version: {platform.python_version()}")
    print(f"Docker SDK version: {docker.__version__}")
    
    # Method 1: Default with no environment variables
    print("\nMethod 1: Default with no environment variables")
    try:
        # Save the current DOCKER_HOST value
        original_docker_host = os.environ.pop('DOCKER_HOST', None)
        client = docker.DockerClient()
        containers = client.containers.list()
        print(f"SUCCESS! Found {len(containers)} containers")
        # Restore the environment variable
        if original_docker_host:
            os.environ['DOCKER_HOST'] = original_docker_host
        return "Method 1", client
    except Exception as e:
        print(f"FAILED: {str(e)}")
        # Restore the environment variable
        if original_docker_host:
            os.environ['DOCKER_HOST'] = original_docker_host
    
    # Method 2: With unix socket (double slash)
    print("\nMethod 2: With unix socket (double slash)")
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        containers = client.containers.list()
        print(f"SUCCESS! Found {len(containers)} containers")
        return "Method 2", client
    except Exception as e:
        print(f"FAILED: {str(e)}")
    
    # Method 3: With unix socket (triple slash)
    print("\nMethod 3: With unix socket (triple slash)")
    try:
        client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
        containers = client.containers.list()
        print(f"SUCCESS! Found {len(containers)} containers")
        return "Method 3", client
    except Exception as e:
        print(f"FAILED: {str(e)}")
    
    # Method 4: With TCP connection
    print("\nMethod 4: With TCP connection")
    try:
        client = docker.DockerClient(base_url='tcp://127.0.0.1:2375')
        containers = client.containers.list()
        print(f"SUCCESS! Found {len(containers)} containers")
        return "Method 4", client
    except Exception as e:
        print(f"FAILED: {str(e)}")
    
    # Method 5: With TCP connection to Docker socket proxy
    print("\nMethod 5: With TCP connection to Docker socket proxy")
    try:
        client = docker.DockerClient(base_url='tcp://127.0.0.1:2376')
        containers = client.containers.list()
        print(f"SUCCESS! Found {len(containers)} containers")
        return "Method 5", client
    except Exception as e:
        print(f"FAILED: {str(e)}")
    
    # Method 6: With environment variable
    print("\nMethod 6: With environment variable")
    try:
        os.environ['DOCKER_HOST'] = 'unix:///var/run/docker.sock'
        client = docker.from_env()
        containers = client.containers.list()
        print(f"SUCCESS! Found {len(containers)} containers")
        return "Method 6", client
    except Exception as e:
        print(f"FAILED: {str(e)}")
    
    # Method 7: With APIClient
    print("\nMethod 7: With APIClient")
    try:
        client = docker.APIClient(base_url='unix:///var/run/docker.sock')
        containers = client.containers()
        print(f"SUCCESS! Found {len(containers)} containers")
        return "Method 7", client
    except Exception as e:
        print(f"FAILED: {str(e)}")
    
    print("\nAll methods failed to connect to Docker.")
    return None, None

if __name__ == "__main__":
    method, client = test_docker_connection_methods()
    
    if method:
        print(f"\nSuccessfully connected to Docker using {method}!")
        print("Container list:")
        for container in client.containers.list(all=True):
            print(f"  - {container.name} (ID: {container.short_id}) - Status: {container.status}")
    else:
        print("\nFailed to connect to Docker using any method.")
        print("Please check that Docker is running and accessible.") 