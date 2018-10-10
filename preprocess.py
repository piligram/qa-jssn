from nltk.tokenize import sent_tokenize
import argparse
import os 
import json

def preprocess(args):
    #데이터셋 폴더 생성
    os.makedirs(args.output_dir, exist_ok=True)

    train_file = os.path.join(args.input_dir, args.input_file)

    with open(train_file, 'r', encoding='utf-8') as f:
        data = json.load(f)['data']

    count = 0
    contexts = {}
    for i in range(len(data)):
        title = data[i]['title']
        paragraph = data[i]['paragraphs']
        print(title)

        with open(os.path.join(args.output_dir, title + ".txt"), 'w', encoding='utf-8') as f:
            for k in range(len(paragraph)):
                contexts = paragraph[k]['context']
                f.write(contexts)
                f.write("\n\n")
                contexts_tokenize = sent_tokenize(contexts)
                for j in range(len(paragraph[k]['qas'])):
                    qas = paragraph[k]['qas'][j]
                    f.write(qas['question'] + "|")
                    if('plausible_answers' in qas):
                        f.write("pa|" )
                        answer = qas['plausible_answers'][0]['text']
                        answer_type = 'plausible_answers'
                        #answers.append(qas['plausible_answers'][0]['text'])
                    else:
                        f.write("a|")
                        answer = qas['answers'][0]['text']
                        answer_type = 'answers'
                    char_answer_start = qas[answer_type][0]['answer_start']
                    char_answer_end = char_answer_start + len(answer)
                    contexts_split = contexts[:char_answer_start].split(" ")
                    word_answer_start = len(contexts_split) - 1
                    word_answer_end = word_answer_start + len(answer.split(" "))
                    for e in range(len(contexts_tokenize)):
                        if answer in contexts_tokenize[e]:
                            sent_answer_start_end = e
                            break;
                    things = "{}|{}|{}|{}|{}|{}".format(answer, char_answer_start, char_answer_end, word_answer_start, word_answer_end, sent_answer_start_end)
                    f.write(things)
                    f.write("\n")
                    count += 1
                f.write("\n")
    print(count)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='hello')

    parser.add_argument('--input_dir', default = "./")
    parser.add_argument('--input_file', default = "train-v2.0.json")
    parser.add_argument('--output_dir', default = "./dataset")
    
    args = parser.parse_args()
    preprocess(args)
