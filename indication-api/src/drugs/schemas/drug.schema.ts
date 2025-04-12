import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';

export type DrugDocument = Drug & Document;

@Schema({ timestamps: true })
export class Drug {
  _id: Types.ObjectId;

  @Prop({ required: true, unique: true })
  setid: string;

  @Prop({ required: true })
  name: string;
}

export const DrugSchema = SchemaFactory.createForClass(Drug); 