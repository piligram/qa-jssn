import json
import tensorflow as tf
import glob
import argparse
import os
import time

def feeder(args):    

    contexts = []
    titles = []
    context_num = []
    questions = []
    answers = []

    input_files = glob.glob(os.path.join(args.input_dir, "*.txt")) 

    for input_file in input_files:  
        with open(input_file, 'r', encoding='utf-8') as f:
            titles.append(input_file[:-4])
            lines = f.readlines()
            for i in range(len(lines)):
                if(len(lines[i].strip()) == 0):
                    continue
                elif(lines[i].count("|") == 7):
                    meta = lines[i].split("|")
                    questions.append(meta[0])
                    answers.append(meta[2])
                    context_num.append(len(contexts) - 1)
                else:
                    contexts.append(lines[i])


    questions_placeholder = tf.placeholder(tf.string)
    answers_placeholder = tf.placeholder(tf.string)

    dataset = tf.data.Dataset.from_tensor_slices((questions_placeholder, answers_placeholder))

    dataset = dataset.batch(1).\
              shuffle(buffer_size=10000).\
              repeat(1)

    iterator = dataset.make_initializable_iterator()

    #iterator = dataset.make_one_shot_iterator()

    next_element = iterator.get_next()
    cc = 0
    with tf.train.MonitoredTrainingSession() as sess:
        sess.run(iterator.initializer, feed_dict={questions_placeholder: questions, answers_placeholder: answers})
        while not sess.should_stop(): 
            cc += 1
            sess.run(next_element)
            if(cc%1000 == 0):
                print(cc)
    print(cc)
    print(len(questions)/32)
 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hello')

    parser.add_argument('--input_dir', default = "./dataset")
    parser.add_argument('--output_dir', default = "./dataset")
    
    args = parser.parse_args()
    feeder(args)
