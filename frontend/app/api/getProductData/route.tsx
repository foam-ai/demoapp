import { NextResponse } from 'next/server';
import path from 'path';
import fs from 'fs/promises';
import { ProductData } from '@/app/types';

export async function GET() {
  try {
    const publicDir = path.join(process.cwd(), 'public/data');
    const categories = await fs.readdir(publicDir);

    const productData: ProductData[] = [];
    const applicationMap: Record<string, { title: string; url: string }[]> = {};

    for (const category of categories) {
      const categoryDir = path.join(publicDir, category);
      const directories = await fs.readdir(categoryDir);

      for (const dir of directories) {
        const dataPath = path.join(categoryDir, dir, 'data.json');
        const jsonData = await fs.readFile(dataPath, 'utf-8');
        const data: ProductData = JSON.parse(jsonData);
        productData.push({ ...data, category, directory: dir });

        for (const application of Object.keys(data.applications)) {
          if (!applicationMap[application]) {
            applicationMap[application] = [];
          }
          applicationMap[application].push({
            title: data.title,
            url: `/products/${category}/${dir}`,
          });
        }
      }
    }

    return NextResponse.json({ productData, applicationMap });
  } catch (error) {
    console.error('Error in getProductData:', error);
    return NextResponse.json({ error: 'Failed to fetch product data' }, { status: 500 });
  }
}
