import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adamax
from torch.optim.lr_scheduler import ExponentialLR
from tqdm import tqdm


class Trainer:
    def __init__(
        self,
        model,
        trainset,
        testset,
        num_epochs=5,
        batch_size=16,
        init_lr=1e-05,
        device="cpu",
    ):
        self.model = model.to(device)
        self.trainset = trainset
        self.testset = testset
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.init_lr = init_lr
        self.device = device
        self.train_loss_per_epoch = []
        self.train_accuracy_per_epoch = []
        self.test_loss_per_epoch = []
        self.test_accuracy_per_epoch = []

    def tune(self):
        """
        Sets a choice of hyperparameters and trains the model.
        Though this is called tune(), you shouldn't actually do a grid tuning loop here (it's called by the autograder, so train() should only happen once).
        You could use this function to do a tuning loop, then once you've found satisfactory settings, remove the loop and call train() with those settings.

        Collaboration note: while you can discuss techniques for improving the model and techniques for hyperparameter tuning, obviously, sharing exact hyperparameter values is off-limits.
        You should work to discover these settings on your own.

        Set the following hyperparameters:
        - self.num_epochs (number of epochs)
        - self.batch_size (number of datapoints per batch)
        - self.init_lr (learning rate)
        - Any additional hyperparameters that you use to train! You can alter many things about this file.
        Then run self.train()
        """
        self.num_epochs = 10
        self.batch_size = 16
        self.init_lr = 0.002
        self.train()

    def run_epoch(self, total, correct, running_loss, data_iterator, train=True):
        """
        Processes a single epoch of data, for training or validation based on the value of 'train'.

        Your task is to implement a standard PyTorch training/validation loop that:
        1. Iterates through the data_iterator to get batches of inputs and labels
        - Move them to currently used device
        2. Performs forward pass through the model
        3. Computes the loss
        4. If in training mode (train=True):
        - Zeros the gradients
        - Performs backpropagation
        - Updates the model parameters using the optimizer
        5. Updates the total samples, correctly predicted samples and running loss parameters
        6. If in training mode (train=True):
        - Updates the data iterator's progress bar with the current loss and accuracy
        7. At the end, if in training mode:
        - Updates the scheduler

        Args:
            total (int): the total number of samples looked at in this epoch
            correct (int): the total number of samples predicted correctly in this epoch
            running_loss (float): the running sum of loss in this epoch
            data_iterator: iterator through the DataLoader (with a progress bar if train=True)
            train (bool): True if used in training, False if used in validation

        Returns:
            total: the total number of samples looked at in this epoch
            correct: the number of samples predicted correctly in this epoch
            running_loss: the running sum of loss for this epoch

        total and correct are provided as args, because in some code snippets, we want to accumulate them over epochs.
        You can just increment those variables. total+=1 for every example you see, correct+=1 for example you get right.

        We have provided a custom Timer class in utils.py that you can call to check how much time you have left for training.
        This is so that you can implement early stopping if you want to, but it's not required, particularly if you are
        trying to debug your training loop on the autograder and want to print custom messages in case Gradescope times out.

        The autograder automatically adds a 10 minute timer to your Trainer object before calling tune(), which you can access with self.timer().
        You can call this timer at any point to see how much time (in seconds) you have left for training.
        If the timer returns 0, then you will know that the 10 minute limit has been reached and you can stop training to avoid a timeout on Gradescope.

        An example of how you might use this timer for early stopping is as follows:
        ```
        for data in data_iterator:
            # ...
            if hasattr(self, "timer") and self.timer() < THRESHOLD:
                print("Time limit reached, stopping training.")
                # Here you can print training stats, etc. for debugging
                break
        ```

        Hint: The optimizer, loss, and scheduler are set in train(). Take a look at train to see how this function is used!
        Hint: If train=True, at the end of each iteration, use data_iterator.set_postfix() with your current loss and accuracy to display them.
        """
        for inputs, labels in data_iterator:

            inputs, labels = inputs.to(self.device), labels.to(self.device)
            outputs = self.model(inputs)
            loss = self.loss_fn(outputs, labels)
            
            if train:
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            
            running_loss += loss.item()
            total += labels.size(0)
            correct += (outputs.argmax(1) == labels).sum().item()
            
            if train:
                data_iterator.set_postfix(loss=loss.item(), accuracy=correct/total)
                
        if train:
            self.scheduler.step()
            
        return total, correct, running_loss

    def train(self):
        trainloader = torch.utils.data.DataLoader(
            self.trainset, batch_size=self.batch_size, shuffle=True, num_workers=2
        )
        testloader = torch.utils.data.DataLoader(
            self.testset, batch_size=self.batch_size, shuffle=False, num_workers=2
        )
        self.loss_fn = nn.CrossEntropyLoss()
        self.optimizer = Adamax(self.model.parameters(), lr=self.init_lr)
        self.scheduler = ExponentialLR(self.optimizer, gamma=0.9)
        for epoch in range(self.num_epochs):
            self.model.train()
            total = 0
            correct = 0
            running_loss = 0
            with tqdm(trainloader, unit="batch", disable=False) as tepoch:
                tepoch.set_description(f"Epoch {epoch + 1}/{self.num_epochs}")
                total, correct, running_loss = self.run_epoch(
                    total, correct, running_loss, tepoch, train=True
                )
            self.train_loss_per_epoch.append(running_loss / len(trainloader))
            self.train_accuracy_per_epoch.append(correct / total)
            self.model.eval()
            with torch.no_grad():
                test_total = 0
                test_correct = 0
                test_loss = 0
                test_total, test_correct, test_loss = self.run_epoch(
                    test_total, test_correct, test_loss, testloader, train=False
                )
                print(
                    f"Epoch {epoch + 1}: Validation Loss: {test_loss / len(testloader):.2f}, Validation Accuracy: {test_correct / test_total:.3f}"
                )
                self.test_loss_per_epoch.append(test_loss / len(testloader))
                self.test_accuracy_per_epoch.append(test_correct / test_total)

    def get_training_history(self):
        return (
            self.train_loss_per_epoch,
            self.train_accuracy_per_epoch,
            self.test_loss_per_epoch,
            self.test_accuracy_per_epoch,
        )

    def predict(self, testloader):
        self.model.eval()
        predict_probs = []
        predictions = []
        ground_truth = []
        with torch.no_grad():
            for data in testloader:
                inputs, labels = data
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                predict_probs.append(F.softmax(outputs, dim=1))
                predictions.append(outputs.argmax(dim=1))
                ground_truth.append(labels)
        return (
            torch.cat(predict_probs).cpu(),
            torch.cat(predictions).cpu(),
            torch.cat(ground_truth).cpu(),
        )
