from director import Director
import utility
import joblib

def main():
    data = joblib.load(utility.TRAIN_TEST_DATA_PATH)
    test_data, test_labels = data["test_data"], data["test_labels"]
    director = Director()
    print("Note that benign data=0 and malicious data=1")
    j = 1
    for i in range(len(test_data.iloc[:20])):
        p = director.run_pipeline(test_data.iloc[i+15])
        print(j, "| prediction:", p[0], "| test label:", test_labels.iloc[i])
        j += 1

if __name__ == "__main__":
    main()