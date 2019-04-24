import numpy as np
import tensorflow as tf


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(model_file)
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph

def read_tensor_from_image_file(raw_file,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):

    image_reader = tf.io.decode_jpeg(raw_file)
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)
    return result

def recognize(model_file, image_file, label_file):
    input_layer='Placeholder'
    output_layer='final_result'
    input_height=224
    input_width=224
    input_mean = 0
    input_std = 255

    graph = load_graph(model_file)
    t = read_tensor_from_image_file(
            image_file,
            input_height=input_height,
            input_width=input_width,
            input_mean=input_mean,
            input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: t
        })
    results = np.squeeze(results)
    top_k = results.argsort()[-5:][::-1]
    labels = str(label_file, 'utf8').split('\n')
    filtered_labels = list(filter(None, labels))
    return {filtered_labels[i]: results[i] for i in top_k}
