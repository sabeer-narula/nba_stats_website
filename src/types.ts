export interface Player {
  name: string;
  salary: number;
  overpaid_metric: number;
  [key: string]: string | number; // This allows for additional dynamic properties
}