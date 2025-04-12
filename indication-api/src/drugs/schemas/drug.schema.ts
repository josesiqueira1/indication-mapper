import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type DrugDocument = Drug & Document;

@Schema({ timestamps: true })
export class Drug {
  @Prop({ required: true, unique: true })
  setid: string;

  @Prop({ required: true })
  description: string;
}

export const DrugSchema = SchemaFactory.createForClass(Drug); 