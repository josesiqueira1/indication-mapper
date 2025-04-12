import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { DrugsService } from './drugs.service';

@Controller('drugs')
export class DrugsController {
  constructor(private readonly drugsService: DrugsService) {}

  @Get()
  findAll() {
    return this.drugsService.findAll();
  }

  @Get(':id')
  findBySetid(@Param('id') id: string) {
    return this.drugsService.findBySetid(id);
  }
}
