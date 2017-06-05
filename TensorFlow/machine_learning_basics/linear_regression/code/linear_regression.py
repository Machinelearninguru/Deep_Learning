import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import xlrd
import matplotlib.pyplot as plt

# Data file provided by the Stanford course CS 20SI: TensorFlow for Deep Learning Research.
# https://github.com/chiphuyen/tf-stanford-tutorials
DATA_FILE = "data/fire_theft.xls"

# read the data from the .xls file.
book = xlrd.open_workbook(DATA_FILE, encoding_override="utf-8")
sheet = book.sheet_by_index(0)
data = np.asarray([sheet.row_values(i) for i in range(1, sheet.nrows)])
num_samples = sheet.nrows - 1

#######################
## Defining flags #####
#######################
tf.app.flags.DEFINE_integer(
    'num_epochs', 50, 'The number of epochs for training the model. Default=50')
# Store all elemnts in FLAG structure!
FLAGS = tf.app.flags.FLAGS


# creating the weight and bias.
# The defined variables will be initialized to zero.
W = tf.Variable(0.0, name="weights")
b = tf.Variable(0.0, name="bias")


#  Creating placeholders for input X and label Y.
def inputs():
    """
    Defining the place_holders.
    :return:
            Returning the data and label lace holders.
    """
    X = tf.placeholder(tf.float32, name="X")
    Y = tf.placeholder(tf.float32, name="Y")
    return X,Y

# Create the prediction.
def inference(X):
    """
    Forward passing the X.
    :param X: Input.
    :return: X*W + b.
    """
    return X * W + b

def loss(X, Y):
    '''
    compute the loss by comparing the predicted value to the actual label.
    :param X: The input.
    :param Y: The label.
    :return: The loss over the samples.
    '''

    # Making the prediction.
    Y_predicted = inference(X)
    return tf.squared_difference(Y, Y_predicted)


# The training function.
def train(loss):
    learning_rate = 0.0001
    return tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)


with tf.Session() as sess:

    # Initialize the variables[w and b].
    sess.run(tf.global_variables_initializer())

    # Get the input tensors
    X, Y = inputs()

    # Return the train loss and create the train_op.
    train_loss = loss(X, Y)
    train_op = train(train_loss)

    # Step 8: train the model
    for epoch_num in range(FLAGS.num_epochs): # run 100 epochs
        for x, y in data:
          train_op = train(train_loss)

          # Session runs train_op to minimize loss
          loss_value,_ = sess.run([train_loss,train_op], feed_dict={X: x, Y: y})

        # Displaying the loss per epoch.
        print('epoch %d, loss=%f' %(epoch_num+1, loss_value))

        # save the values of weight and bias
        wcoeff, bias = sess.run([W, b])


###############################
#### Evaluate and plot ########
###############################
Input_values = data[:,0]
Labels = data[:,1]
Prediction_values = data[:,0] * wcoeff + bias
plt.plot(Input_values, Labels, 'ro', label='main')
plt.plot(Input_values, Prediction_values, label='Predicted')

# Saving the result.
plt.legend()
plt.savefig('plot.png')
plt.close()
