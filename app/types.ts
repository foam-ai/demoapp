// TODO(Perla):  In the future, break down this file into files. e.g. types/props or types/objects.
export interface Product {
    id: string;
    title: string;
    type: string;
    description: string;
    manufacturer: string;
    payload: string;
    reach: string;
    axes: string;
    images_url: string[];
}

export interface ProductData {
  title: string;
  description: string;
  manufacturer: string;
  url: string;
  applications: Record<string, string>;
  specifications: Record<string, string>;
  images_source_url: string[];
  pdf_source_url: string;
  created_at: number;
  directory?: string;
  category?: string;
}


export interface DigitalInventoryProduct {
    axes: number;
    description: string;
    specifications: { type: string }
    title: string;
    type: string;
    manufacturer: string;
    payload: string;
    reach: string;
    images_url: string[];
}
  
export type Result = {
    source: string,
    condition: string;
    mounting: string;
    axes: string;
    reach: string;
    payload: string;
    quantity: string;
    title: string;
    price: string;
    description: string;
    weight: string;
    url: string;
    extra_information: string;
}


export interface Quote {
    quote_id: string;
    request_id: string;
    source: string;
    title: string;
    url: string;
    price: string;
    delivery_time: string;
    condition?: string;
    mounting?: string;
    axes?: string;
    reach?: string;
    payload?: string;
    description?: string;
    weight?: string;
  }


export interface ContactUsProps {
  onClose?: () => void;
}

export type SearchBarProps = {
    query: string;
    setQuery: (query: string) => void;
    performSearch: () => void;
}

export interface FilterSectionProps {
  label: string;
  element: React.ReactNode;
  range?: number[];
}

export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}

export interface ProductCardProps {
  product: Product;
}

export type ResultCardProps = {
  result: Result;
}


export type ResultsGridProps = {
  results: Result[];
}

export interface RequestQuotePropsProduct {
  title: string;
  description: string;
  payload: string;
  manufacturer: string;
  specifications: { type: string }
}

export interface RequestQuoteProps {
  onClose: () => void;
  product: RequestQuotePropsProduct;
}

export interface User {
  name?: string;
  email?: string;
  sub?: string;
}

export interface UserLoaderProps {
  user: User | null;
  setUser: (user: User | null) => void;
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
  error: Error | null;
  setError: (error: Error | null) => void;
}

export interface Request {
  request_id: string;
  product_name: string;
  serial_number?: string;
  product_link?: string;
  quantity?: number;
  description: string;
  created_at: number;
  images: string[];
  status: string;  // TODO(Perla): Make enum out of this.
}
