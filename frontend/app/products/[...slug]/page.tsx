import { promises as fs } from 'fs';
import path from 'path';
import { ProductData } from '../../../app/types';
import ProductPageClient from './ProductPageClient';

interface ProductPageProps {
  params: { slug: string[] };
}

export async function generateStaticParams() {
  const publicDir = path.join(process.cwd(), 'public/data');
  const categories = await fs.readdir(publicDir);
  const paths: { slug: string[] }[] = [];

  for (const category of categories) {
    const categoryDir = path.join(publicDir, category);
    const directories = await fs.readdir(categoryDir);
    directories.forEach((directory) => {
      paths.push({ slug: [category, directory] });
    });
  }

  return paths;
}

async function getProductData(slug: string[]) {
  const [category, directory] = slug;
  const dataPath = path.join(process.cwd(), 'public', 'data', category, directory, 'data.json');
  const jsonData = await fs.readFile(dataPath, 'utf-8');
  return JSON.parse(jsonData) as ProductData;
}

export default async function ProductPage({ params }: ProductPageProps) {
  const product = await getProductData(params.slug);
  const directory = `${params.slug[0]}/${params.slug[1]}`;
  const imageUrls = [`/data/${directory}/image0.png`, `/data/${directory}/image1.png`];
  const pdfUrl = `/data/${directory}/specs.pdf`;

  return <ProductPageClient product={product} imageUrls={imageUrls} pdfUrl={pdfUrl} />;
}
