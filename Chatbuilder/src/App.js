import React from 'react';
import './App.css';
import { createStore, applyMiddleware } from 'redux';
import { Provider } from 'react-redux';
import ReduxThunk from 'redux-thunk';
import reducers from './reducers';
import 'bootstrap/dist/css/bootstrap.min.css';
import Builder from './screens/Builder';

export const store = createStore(reducers, {}, applyMiddleware(ReduxThunk));

function App() {
  return (
    <Provider store={store}>
      <Builder/>
    </Provider>
  );
}

export default App;
