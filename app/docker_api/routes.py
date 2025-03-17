import docker
from flask import jsonify, request, current_app, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.docker_api import bp
from app.docker_api.forms import ContainerForm

@bp.route('/containers')
@login_required
def containers():
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        containers = client.containers.list(all=True)
        return render_template('docker/containers.html', title='Containers', containers=containers)
    except docker.errors.DockerException as e:
        flash(f'Error connecting to Docker: {str(e)}', 'danger')
        return render_template('docker/containers.html', title='Containers', containers=[])

@bp.route('/container/<container_id>')
@login_required
def container_detail(container_id):
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        container = client.containers.get(container_id)
        return render_template('docker/container_detail.html', title=f'Container: {container.name}', container=container)
    except docker.errors.NotFound:
        flash('Container not found', 'danger')
        return redirect(url_for('docker.containers'))
    except docker.errors.DockerException as e:
        flash(f'Error connecting to Docker: {str(e)}', 'danger')
        return redirect(url_for('docker.containers'))

@bp.route('/container/<container_id>/start', methods=['POST'])
@login_required
def start_container(container_id):
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        container = client.containers.get(container_id)
        container.start()
        flash(f'Container {container.name} started successfully', 'success')
    except docker.errors.NotFound:
        flash('Container not found', 'danger')
    except docker.errors.DockerException as e:
        flash(f'Error starting container: {str(e)}', 'danger')
    
    return redirect(url_for('docker.containers'))

@bp.route('/container/<container_id>/stop', methods=['POST'])
@login_required
def stop_container(container_id):
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        container = client.containers.get(container_id)
        container.stop()
        flash(f'Container {container.name} stopped successfully', 'success')
    except docker.errors.NotFound:
        flash('Container not found', 'danger')
    except docker.errors.DockerException as e:
        flash(f'Error stopping container: {str(e)}', 'danger')
    
    return redirect(url_for('docker.containers'))

@bp.route('/container/<container_id>/restart', methods=['POST'])
@login_required
def restart_container(container_id):
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        container = client.containers.get(container_id)
        container.restart()
        flash(f'Container {container.name} restarted successfully', 'success')
    except docker.errors.NotFound:
        flash('Container not found', 'danger')
    except docker.errors.DockerException as e:
        flash(f'Error restarting container: {str(e)}', 'danger')
    
    return redirect(url_for('docker.containers'))

@bp.route('/container/<container_id>/remove', methods=['POST'])
@login_required
def remove_container(container_id):
    if not current_user.is_admin:
        flash('You do not have permission to remove containers', 'danger')
        return redirect(url_for('docker.containers'))
    
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        container = client.containers.get(container_id)
        container_name = container.name
        container.remove(force=True)
        flash(f'Container {container_name} removed successfully', 'success')
    except docker.errors.NotFound:
        flash('Container not found', 'danger')
    except docker.errors.DockerException as e:
        flash(f'Error removing container: {str(e)}', 'danger')
    
    return redirect(url_for('docker.containers'))

@bp.route('/container/<container_id>/logs')
@login_required
def container_logs(container_id):
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        container = client.containers.get(container_id)
        logs = container.logs(tail=100).decode('utf-8')
        return render_template('docker/logs.html', title=f'Logs: {container.name}', container=container, logs=logs)
    except docker.errors.NotFound:
        flash('Container not found', 'danger')
        return redirect(url_for('docker.containers'))
    except docker.errors.DockerException as e:
        flash(f'Error getting logs: {str(e)}', 'danger')
        return redirect(url_for('docker.containers'))

@bp.route('/images')
@login_required
def images():
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        images = client.images.list()
        return render_template('docker/images.html', title='Images', images=images)
    except docker.errors.DockerException as e:
        flash(f'Error connecting to Docker: {str(e)}', 'danger')
        return render_template('docker/images.html', title='Images', images=[])

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_container():
    if not current_user.is_admin:
        flash('You do not have permission to create containers', 'danger')
        return redirect(url_for('docker.containers'))
    
    form = ContainerForm()
    
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        images = [(image.tags[0] if image.tags else image.short_id) for image in client.images.list()]
        form.image.choices = [(image, image) for image in images]
    except docker.errors.DockerException as e:
        flash(f'Error connecting to Docker: {str(e)}', 'danger')
        form.image.choices = []
    
    if form.validate_on_submit():
        try:
            ports = {}
            if form.ports.data:
                port_mappings = form.ports.data.split(',')
                for mapping in port_mappings:
                    if ':' in mapping:
                        host_port, container_port = mapping.strip().split(':')
                        ports[container_port] = int(host_port)
            
            environment = {}
            if form.environment.data:
                env_vars = form.environment.data.split(',')
                for env_var in env_vars:
                    if '=' in env_var:
                        key, value = env_var.strip().split('=', 1)
                        environment[key] = value
            
            client.containers.run(
                form.image.data,
                name=form.name.data,
                detach=True,
                ports=ports,
                environment=environment
            )
            
            flash(f'Container {form.name.data} created successfully', 'success')
            return redirect(url_for('docker.containers'))
        except docker.errors.DockerException as e:
            flash(f'Error creating container: {str(e)}', 'danger')
    
    return render_template('docker/create.html', title='Create Container', form=form)

@bp.route('/api/containers')
@login_required
def api_containers():
    try:
        client = docker.DockerClient(base_url=current_app.config['DOCKER_HOST'])
        containers = client.containers.list(all=True)
        
        container_list = []
        for container in containers:
            container_list.append({
                'id': container.short_id,
                'name': container.name,
                'image': container.image.tags[0] if container.image.tags else container.image.short_id,
                'status': container.status,
                'created': container.attrs['Created'],
                'ports': container.ports
            })
        
        return jsonify(container_list)
    except docker.errors.DockerException as e:
        return jsonify({'error': str(e)}), 500 