import docker
import os
import platform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_docker_connection():
    try:
        # Get Docker host from environment or use default based on platform
        docker_host = os.environ.get('DOCKER_HOST')
        
        print(f"Using Docker host: {docker_host}")
        
        # Try different connection methods
        print("Method 1: Using docker.from_env()")
        try:
            client1 = docker.from_env()
            containers1 = client1.containers.list()
            print(f"Method 1 Success! Found {len(containers1)} containers")
        except Exception as e:
            print(f"Method 1 Failed: {str(e)}")
        
        print("\nMethod 2: Using DockerClient with explicit base_url")
        try:
            client2 = docker.DockerClient(base_url='unix:///var/run/docker.sock')
            containers2 = client2.containers.list()
            print(f"Method 2 Success! Found {len(containers2)} containers")
        except Exception as e:
            print(f"Method 2 Failed: {str(e)}")
            
        print("\nMethod 3: Using APIClient directly")
        try:
            client3 = docker.APIClient(base_url='unix:///var/run/docker.sock')
            containers3 = client3.containers()
            print(f"Method 3 Success! Found {len(containers3)} containers")
        except Exception as e:
            print(f"Method 3 Failed: {str(e)}")
            
        return True
    except Exception as e:
        print(f"General error: {str(e)}")
        return False

if __name__ == "__main__":
    # Print environment variables and system info for debugging
    print(f"Platform: {platform.system()}")
    print(f"DOCKER_HOST: {os.environ.get('DOCKER_HOST', 'Not set')}")
    print(f"Python version: {platform.python_version()}")
    print(f"Docker SDK version: {docker.__version__}")
    print("\nTesting Docker connection methods:")
    
    # Test the connection
    test_docker_connection() 