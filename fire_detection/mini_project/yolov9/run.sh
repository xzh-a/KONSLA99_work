# train yolov9 models
# python train_dual.py --workers 8 --device 0 --batch 16 --data ../data/mini_project/data.yaml --img 640 --nosave --cfg models/detect/yolov9-c.yaml --weights '' --name test-yolov9-c --hyp hyp.scratch-high.yaml --min-items 0 --epochs 300 --close-mosaic 15 >> ./result/yolov9.txt

# train gelan models
# python train.py --workers 8 --device 0 --batch 32 --data ../data/mini_project/data.yaml --img 640 --cfg models/detect/gelan-c.yaml --weights '' --name gelan-c --hyp hyp.scratch-high.yaml --min-items 0 --epochs 300 --close-mosaic 15 >> ./result/gelanc.txt


#test img
# inference converted yolov9 models
#python detect.py --source './data/images/horses.jpg' --img 640 --device 0 --weights './yolov9-c-converted.pt' --name yolov9_c_c_640_detect

# inference yolov9 models
# python detect_dual.py --source './data/images/test1.jpg' --img 640 --device 0 --weights 'yolov9/runs/train/test-yolov9-c17/weights/last.pt' --name yolov9_17_detect

# inference gelan models
# python detect.py --source './data/images/test1.jpg' --img 640 --device 0 --weights 'yolov9/runs/train/gelan-c2/weights/best.pt' --name gelan_2_detect


#shell programming - run detect for 6 images

# for ((i=1; i<=6; i++)); do
#     # inference yolov9 models
#     python detect_dual.py --source "./data/images/test${i}.jpg" --img 640 --device 0 --weights './runs/train/test-yolov9-c17/weights/last.pt' --name yolov9_17_detect

#     # inference gelan models
#     python detect.py --source "./data/images/test${i}.jpg" --img 640 --device 0 --weights './runs/train/gelan-c2/weights/best.pt' --name gelan_2_detect
# done


# for ((i=1; i<=2; i++)); do
#     # inference yolov9 models
#     python detect_dual.py --source "./data/images/test${i}.jpg" --img 640 --device 0 --weights './runs/train/test-yolov9-c17/weights/last.pt' --name yolov9_17_detect --save-txt --save-conf 

#     # inference gelan models
#     python detect.py --source "./data/images/test${i}.jpg" --img 640 --device 0 --weights './runs/train/gelan-c2/weights/best.pt' --name gelan_2_detect --save-txt --save-conf
# done

# python train_dual.py --workers 8 --device 0 --batch 16 --flat-cos-lr --data ../data/mini_project/data.yaml --img 640 --nosave --cfg models/detect/yolov9-c.yaml --weights '' --name yolov9 --hyp hyp.scratch-high.yaml --min-items 0 --epochs 500 --close-mosaic 15 

# python train_dual.py --workers 8 --device 0 --batch 16 --data ../data/mini_project/data.yaml --img 640 --nosave --cfg models/detect/yolov9-c.yaml --weights '' --name yolov9 --hyp hyp.scratch-high.yaml --min-items 0 --epochs 500 --close-mosaic 15 

# #python train_dual.py --workers 8 --device 0 --batch 32 --data ../data/mini_project/data.yaml --img 640 --nosave --cfg models/detect/yolov9-c.yaml --weights '' --name yolov9_32batch --hyp hyp.scratch-high.yaml --min-items 0 --epochs 500 --close-mosaic 15 
# #-> batch 32 : cuda out of memory
# python train_dual.py --workers 8 --device 0 --batch 16 --cos-lr --data ../data/mini_project/data.yaml --img 640 --nosave --cfg models/detect/yolov9-c.yaml --weights '' --name yolov9 --hyp hyp.scratch-high.yaml --min-items 0 --epochs 500 --close-mosaic 15 


# evaluate yolov9 models

python val_dual.py --data ../data/mini_project/data.yaml --img 640 --batch 32 --conf 0.001 --iou 0.7 --device 0 --weights './runs/train/yolov9_fine/weights/best.pt' --name yolov9_fine_prun

python val_dual.py --data ../data/mini_project/data.yaml --img 640 --batch 32 --conf 0.001 --iou 0.7 --device 0 --weights './runs/train/yolov9_dynamic_prun/weights/last.pt' --name yolov9_dyn_prun

python val_dual.py --data ../data/mini_project/data.yaml --img 640 --batch 32 --conf 0.001 --iou 0.7 --device 0 --weights './runs/train/yolov9_fine_source/weights/last.pt' --name yolov9_fine_src

#fine_tuning (w. pruning)
#python fine_tuning.py --workers 8 --device 0 --batch 16 --cos-lr --data ../data/mini_project/data.yaml --img 640 --nosave --cfg models/detect/yolov9-c.yaml --weights ./runs/train/yolov94/weights/last.pt --name yolov9 --hyp hyp.scratch-high.yaml --min-items 0 --epochs 200 --close-mosaic 15 --noval