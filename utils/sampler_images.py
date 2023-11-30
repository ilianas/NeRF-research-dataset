import os
import os.path as osp
import shutil
from sklearn.model_selection import ShuffleSplit, train_test_split
import argparse
import numpy as np

def split_into_n_groups(X, n_groups):
    # Shuffle the indices
    shuffled_indices = np.random.permutation(len(X))
    
    # Split the indices into n groups
    split_indices = np.array_split(shuffled_indices, n_groups)
    
    groups = [[X[i] for i in indices] for indices in split_indices]
    
    return groups

def main(args):
    dir2save = args.dir2save
    n_splits = args.n_splits
    one_extraction_size = args.one_extraction_size
    dir2sampels_main = args.dir2sampels_main

    dir2imags = osp.join(dir2sampels_main, "images")
    print(osp.exists(dir2imags))
    assert osp.exists(dir2imags), f"images folder doesn't exist: {dir2imags}"

    name = osp.basename(dir2sampels_main)
    dir2save_new = osp.join(dir2save, f"{name}_splitted")

    os.makedirs(dir2save_new, exist_ok=True)
    shutil.rmtree(dir2save_new)
    os.makedirs(dir2save_new, exist_ok=True)

    imgs = os.listdir(dir2imags)
    
    if (n_splits is not None) and (one_extraction_size is not None):
        print(f"set only one of them: n_splits or one_extraction_size")
        return
    
    if n_splits is not None:
        test = []
        for i, train_index in enumerate(split_into_n_groups(imgs, n_splits)):
            print(train_index)
            dir2sample = os.path.join(dir2save_new, f"{name}_splitted_group_n_{i+1}/images")
            os.makedirs(dir2sample, exist_ok=True)
            shutil.rmtree(dir2sample)
            os.makedirs(dir2sample, exist_ok=True)
            for img in train_index:
                shutil.copy(osp.join(dir2imags, img), dir2sample)
            
            print(set(test) & set(train_index))
            test.extend(train_index)
                
    elif one_extraction_size is not None:
        assert .0 <= one_extraction_size <= 1., f".0 <= {one_extraction_size} <= 1."
        subset, _ = train_test_split(imgs, test_size=1-one_extraction_size, random_state=42, shuffle=True)

        dir2sample = os.path.join(dir2save_new, f"{name}_one_random_extraction_size_{str(one_extraction_size).replace('.', '_')}/images")
        os.makedirs(dir2sample, exist_ok=True)
        shutil.rmtree(dir2sample)
        os.makedirs(dir2sample, exist_ok=True)
        for img in subset:
            shutil.copy(osp.join(dir2imags, img), dir2sample)
    else:
        print(f"set one of them: n_splits or one_extraction_size")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to split dataset")
    parser.add_argument("--dir2sampels_main", type=str, required=True, help="Main directory with samples")
    parser.add_argument("--dir2save", type=str, required=True, help="Directory to save results")
    parser.add_argument("--one_extraction_size", type=float, default=None, help="Size for one extraction")
    parser.add_argument("--n_splits", type=int, default=None, help="Number of splits")
    
    args = parser.parse_args()
    main(args)
