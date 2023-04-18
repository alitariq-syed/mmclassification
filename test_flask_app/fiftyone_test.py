#%%
import fiftyone as fo


# Create a dataset from a local directory
# dataset = fo.Dataset.from_dir('G:/TBX11K/TBX11K/imgs/tb', fo.types.ImageClassificationDirectoryTree)
dataset = fo.Dataset.from_dir(r'G:\mmclassification\test_flask_app\data', fo.types.ImageClassificationDirectoryTree)
# dataset.explore()
session = fo.launch_app(dataset)
session.wait()
export_dir = '/test/output'
label_field = "ground_truth"
dataset.export(
        export_dir=export_dir,
    dataset_type=fo.types.ImageClassificationDirectoryTree,
    label_field=label_field,
)
# samples = session.view()
# print(samples)
# Export the dataset
# dataset.export(
#     export_dir=export_dir,
#     dataset_type=dataset_type,
#     label_field=label_field,
# )

#%%

# Export the samples in the dataset to different directories based on their tags or labels
# for label in session.dataset.aggregate_labels():
#     query = {'$in': [label]}
#     subset = session.dataset.filter_labels('tags', query)
#     output_dir = f'/test/output/{label}'
#     subset.export(output_dir)


#%%
# import fiftyone as fo
# import fiftyone.zoo as foz

# dataset = foz.load_zoo_dataset("quickstart")
# session = fo.launch_app(dataset)
# session.wait()

# %%
# import fiftyone as fo
# import fiftyone.zoo as foz

# dataset = foz.load_zoo_dataset("quickstart")
# session = fo.launch_app(dataset)