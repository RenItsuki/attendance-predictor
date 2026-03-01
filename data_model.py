import math
import csv

#for getting values in terms of probalibily (between 0 to 1)
def sigmoid(z):
    return 1/(1+math.exp(-z))
#for getting the perdiction
def predict(features):
    p=bias+sum(float(w)*float(f) for w,f in zip(weights,features))
    return sigmoid(p)

def train(file):
#accessing data in file STD.csv
    d_l=[]
    o=open(file,"r")
    data=csv.reader(o)
    for i in data:
        if i!=[]:
            d_l.append(i)
    o.close()
#exaction
    x=[r[:-1] for r in d_l]
    y=[r[-1] for r in d_l]
#starting weights and bias
    global weights, bias
    weights= [0.0]*len(x[0])
    bias= 0.0
#learing rate and no of iterations
    l_r=0.01
    n_it=50000
#training model
    for it in range(n_it):
        predictions=[predict(features) for features in x]
        grad_weights=[0.0]*len(weights) #for gradient development of the weight
        grad_bias=0.0 #for gradient development of bias
#learning and developing gradients
        for i in range(len(x)):
            er=predictions[i]-float(y[i])
            for j in range(len(weights)):
                grad_weights[j]+=er*float(x[i][j])
            grad_bias+=er
#Update weight and bias
        weights = [w-l_r*g_w/len(x) for w,g_w in zip(weights,grad_weights)]
        bias -= l_r*grad_bias/len(x)
#After Trainging, the final weigthts ans bias
    t_out=[weights,bias,x,y]
    return(t_out)
#final_prediction
def f_predict(n_d,t_out):
    weights=t_out[0]
    bias=t_out[1]
    x=t_out[2]
    y=t_out[3]
    p=predict(n_d)
    l_d=n_d
    l_d.append(p)
#calculate accuracy
    predictions = [predict(features) for features in x]
    c_p = sum(1 for p, at in zip(predictions, y) if abs(p-float(at)) <= 0.11)
    ar=c_p/len(y)
    f_out=[p,ar]
    return(f_out)
