export interface Recipes {
    status:  boolean;
    message: string;
    data:    Datum[];
}

export interface Datum {
    id:           number;
    name:         string;
    slug:         string;
    description:  string;
    time:         string;
    image:        string;
    created_date: string;
    category:     string;
    category_id:  number;
    user_id:      number;
    user:         string;
}
