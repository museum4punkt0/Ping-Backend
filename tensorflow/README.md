# Image Classification Tutorial - TensorFlow!
You can generate both mobile or backend graphs with files is directories of this repo

 ## Setup and Install
 - Python 2.7
 - clone the project
 - add folders with images to classify into a dataset/ directory, forlders names results into labels name file (see two example directories in dataset)
 - cd backend_graph/ or mobile_graph/ 
 
 - Create virtual environment, if you want using virtualenv command
 - Install dependent libararies
   > pip install -r requirements.txt
 
 ## Train your model using our processed dataset
 - Run the below command to train your model using different architectures.
   For mobile graph
   > python retrain.py \
    --image_dir /home/user/Documents/projects/deep-learning/dataset/ \
    --architecture=mobilenet_1.0_224 \
    --output_graph=trained_model/museum_mobile_v1_224_graph.pb \
    --output_labels=labels/museum_mobile_1_224_labels_2.txt

   For backend graph
   > python retrain.py \
    --image_dir /home/user/Documents/projects/deep-learning/dataset/ \
    --tfhub_module https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2 \
    --output_graph=trained_model/example_backend_mobile_v2_224_graph.pb \
    --output_labels=labels/example_backend_mobile_v2_224_labels.txt 
         

  ## Test your model
  - Run the below python script to classify your test images based on our pre-trained model.
  > python label_image.py \
    --graph=trained_model/example_backend_mobile_v2_224_graph.pb \
    --labels=labels/example_backend_mobile_v2_224_labels.txt \
    --image=label_image/image you want to classify.jpg \
    --input_layer=Placeholder \
    --output_layer=final_result \
    --input_mean=128 \
    --input_std=128 \
    --input_width=224 \
    --input_height=224

 ## Done.
  
  
 
