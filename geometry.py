def centered(container,  object_size):
    container_x, container_y, container_w, container_h = container
    object_width, object_height = object_size
    x = container_x + int((container_w - object_width) / 2)
    y = container_y + int((container_h - object_height) / 2)
    return x, y
