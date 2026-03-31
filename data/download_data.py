import kagglehub

# download latest version
path = kagglehub.dataset_download("desolution01/messy-employee-dataset")

print("Path to dataset files:", path)