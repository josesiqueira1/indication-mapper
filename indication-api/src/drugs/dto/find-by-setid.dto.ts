import { IsNotEmpty, IsString } from 'class-validator';

export class FindBySetidDto {
  @IsString()
  @IsNotEmpty()
  setid: string;
} 