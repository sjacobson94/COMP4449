from sklearn.model_selection import GridSearchCV
import time

# updated function to be flexible with regression and classification as well as other scoring functions
# and to include the option for one of the voting models from sklearn
def best_model(X_train, y_train, X_test, y_test, models, params, scoring_function, transformer=None, ensemble_model=None, cv_scoring_metric="accuracy", folds=5):
    # initializing some variables to store models and predictions in
    best_mods, train_preds, test_preds, train_accs, test_accs, fit_times = [], [], [], [], [], []
    # transforming the train and test datasets
    if transformer:
        X_train_transformed = transformer.fit_transform(X_train)
        X_test_transformed = transformer.transform(X_test)
    else: 
        X_train_transformed = X_train
        X_test_transformed = X_test
    # looping through the models
    for (name, clf), parms in zip(models.items(), params):
        start = time.time()
        # using GridSearchCV to find the optimal parameters for the data
        grid = GridSearchCV(estimator = clf, param_grid = parms, n_jobs = -1, cv = folds, verbose=True, scoring=cv_scoring_metric)
        # grid = RandomizedSearchCV(estimator = clf, param_distributions = parms, n_jobs = -1, cv = 5, verbose=True, n_iter=20, random_state=42)
        grid.fit(X_train_transformed, y_train)
        end = time.time()
        fit_times.append(end-start)
        best_mod = grid.best_estimator_
        # creating predictions
        train_pred = best_mod.predict(X_train_transformed)
        test_pred = best_mod.predict(X_test_transformed)
        # calculating and printing fitting metric
        train_acc = scoring_function(y_train, train_pred)
        test_acc = scoring_function(y_test, test_pred)
        print(f"%s Training Metric: %s, Test Metric: %s\n" % (name, train_acc, test_acc), sep='')
        # storing predictions and best CV models
        train_accs.append(train_acc)
        test_accs.append(test_acc)
        train_preds.append(train_pred)
        test_preds.append(test_pred)
        best_mods.append(best_mod)
    if ensemble_model:
        if ensemble_model.__name__ == "VotingRegressor":
            # fitting the soft voting classifier as the ensemble model but not including those way overfit, i.e. accuracy=1
            voting = ensemble_model([
                    (name, mod) for name, mod, acc in zip(models.keys(), best_mods, train_accs)
                ], n_jobs=-1)
            # hard voting
            start = time.time()
            voting.fit(X_train_transformed, y_train)
            end = time.time()
            fit_times.append(end-start)
            train_pred = voting.predict(X_train_transformed)
            test_pred = voting.predict(X_test_transformed)
            train_acc = scoring_function(y_train, train_pred)
            test_acc = scoring_function(y_test, test_pred)
            print(f"%s Training Metric: %s, Test Metric: %s\n" % (ensemble_model.__name__, train_acc, test_acc), "\n", sep='')
            train_accs.append(train_acc)
            test_accs.append(test_acc)
            train_preds.append(train_pred)
            test_preds.append(test_pred)
            best_mods.append(voting_hard)
        elif ensemble_model.__name__ == "VotingClassifier":
            # fitting the hard voting classifier as the ensemble model
            voting_hard = ensemble_model([
                    (name, mod) for name, mod in zip(models.keys(), best_mods) #if (hasattr(mod, "predict_proba") and voting == "soft") or voting == 'hard'
                ], voting="hard", n_jobs=-1)
            # fitting the soft voting classifier as the ensemble model but not including those way overfit, i.e. accuracy=1
            voting_soft = ensemble_model([
                    (name, mod) for name, mod, acc in zip(models.keys(), best_mods, train_accs) if hasattr(mod, "predict_proba") and acc < 1
                ], voting="soft", n_jobs=-1)
            # hard voting
            start = time.time()
            voting_hard.fit(X_train_transformed, y_train)
            end = time.time()
            fit_times.append(end-start)
            train_pred = voting_hard.predict(X_train_transformed)
            test_pred = voting_hard.predict(X_test_transformed)
            train_acc = scoring_function(y_train, train_pred)
            test_acc = scoring_function(y_test, test_pred)
            print(f"VotingClassifier_Hard Training Metric: %s, Test Metric: %s" % (train_acc, test_acc), sep='')
            train_accs.append(train_acc)
            test_accs.append(test_acc)
            train_preds.append(train_pred)
            test_preds.append(test_pred)
            best_mods.append(voting_hard)
            # soft voting
            start = time.time()
            voting_soft.fit(X_train_transformed, y_train)
            end = time.time()
            fit_times.append(end-start)
            train_pred = voting_soft.predict(X_train_transformed)
            test_pred = voting_soft.predict(X_test_transformed)
            train_acc = scoring_function(y_train, train_pred)
            test_acc = scoring_function(y_test, test_pred)
            print(f"VotingClassifier_Soft Training Metric: %s, Test Metric: %s\n" % (train_acc, test_acc), sep='')
            train_accs.append(train_acc)
            test_accs.append(test_acc)
            train_preds.append(train_pred)
            test_preds.append(test_pred)
            best_mods.append(voting_soft)
    # storing all of the models/predictions/metrics/data in a dictionary
    out = {
        "best_models": best_mods,
        "train_accuracy": train_accs,
        "test_accuracy": test_accs,
        "fit_times": fit_times, 
        "train_preds": train_preds,
        "test_preds": test_preds,
        "X_train_transformed": X_train_transformed,
        "X_test_transformed": X_test_transformed,
        "transformer": transformer
    }
    # return predictions, models, and transformed data
    return(out)


# more specific function designed to loop through the season in the data
# to fit models for each. Used in a {key:function(year) for year in range()}
# call
def fit_optimize_season_model(data, year, models, transformer, params, accuracy_score, ensemble_model):
    season = str(year)+'/'+str(year+1)
    print(f"Fitting models for the %s season\n" % season)
    # data split specified season
    X_train, X_test = data[data.season.str[0:4].astype(int) < year].drop(columns=["gameID", "season", "homeTeamWin", "venue"]), \
                      data[data.season.str[0:4].astype(int) == year].drop(columns=["gameID", "season", "homeTeamWin", "venue"])
    
    y_train, y_test = data[data.season.str[0:4].astype(int) < year]['homeTeamWin'], \
                      data[data.season.str[0:4].astype(int) == year]['homeTeamWin']
    
    start = time.time()
    
    fit_mods = best_model(
        X_train = X_train, 
        y_train = y_train, 
        X_test = X_test, 
        y_test = y_test, 
        models = models, 
        transformer = transformer, 
        params = params,
        scoring_function = accuracy_score,
        cv_scoring_metric = "accuracy",
        ensemble_model = ensemble_model,
        folds = 5
    )
    
    end = time.time()
    print("Model fitting for the ", season, " season took: ", end - start, " seconds\n", sep='')
    # adding a few more things to differentiate each season because of the different data
    fit_mods['X_train'] = X_train
    fit_mods['X_test'] = X_test
    fit_mods['y_train'] = y_train
    fit_mods['y_test'] = y_test
    fit_mods['season'] = [str(year)+'/'+str(year+1) for i in fit_mods["best_models"]]
    # return the dictionary of data/models
    return(fit_mods)

