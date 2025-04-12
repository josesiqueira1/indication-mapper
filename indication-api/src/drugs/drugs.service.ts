import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Drug, DrugDocument } from './schemas/drug.schema';

@Injectable()
export class DrugsService {
  constructor(@InjectModel(Drug.name) private userModel: Model<DrugDocument>) {}

  async findAll(): Promise<Drug[]> {
    return this.userModel.find().exec();
  }

  async findBySetid(id: string): Promise<Drug | null> {
    return this.userModel.findOne({ setid: id }).exec();
  }
}
