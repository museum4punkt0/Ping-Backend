import express from 'express';
import http from 'http';
import bodyParser from 'body-parser';
import cookieParser from 'cookie-parser';
import mongoose from 'mongoose';
import logger from 'morgan';
import path from 'path';
import routes from './api/v1';
import remote from './constants';

// Set up the express app
const app = express();
const server = http.createServer(app);

const PORT = 5000;

app.use(logger('dev'));
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use('/assets', express.static(path.join(__dirname, 'assets')));


// Routes:
app.use(`${remote.API_ROUTE}/signin`, routes.signin);
app.use(`${remote.API_ROUTE}/signup`, routes.signup);
app.use(`${remote.API_ROUTE}/dialogues`, routes.dialogues);
app.use(`${remote.API_ROUTE}/objekts`, routes.objekts);
app.use(`${remote.API_ROUTE}/character`, routes.character);

mongoose.set('debug', true);
mongoose.connect('mongodb://localhost:27017/MeinObjekt', { useNewUrlParser: true })
  .then(() => server.listen(PORT, () => console.log(`Server running on port ${PORT}`)))
  .catch(() => console.error('Error: Server cannot start without mongo'));
