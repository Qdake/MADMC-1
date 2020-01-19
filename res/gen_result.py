with open("ND_20_4.txt","r") as f:
    data = [line.split(':') for line in f]
    temp_data = [float(i[1]) for i in data if "Temps d'execution" in i[0]]
    gap_data = [float(i[1]) for i in data if "gap:" in i[0]]
    question_data = [float(i[1]) for i in data if "Nombre de question:" in i[0]]
    print("temp: {}; gap: {} ; question_data: {} ".format(sum(temp_data)/len(temp_data),
          sum(gap_data)/len(gap_data),sum(question_data)/len(question_data)));