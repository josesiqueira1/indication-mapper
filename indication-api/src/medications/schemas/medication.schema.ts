import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';

export type MedicationDocument = Medication & Document;

@Schema({ timestamps: true })
export class Medication {
  _id: Types.ObjectId;

  @Prop({ required: true, unique: true })
  setid: string;

  @Prop({ required: true })
  description: string;
}

export const MedicationSchema = SchemaFactory.createForClass(Medication); 