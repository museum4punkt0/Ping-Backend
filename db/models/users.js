import mongoose, { Schema } from 'mongoose';

const UsersSchema = new Schema({
  username: { type: String },
  password: { type: String },
  registeredAt: { type: Date, default: Date.now },
},
{ versionKey: false, collection: 'UsersCollection' });


export default mongoose.model('UsersModel', UsersSchema);
