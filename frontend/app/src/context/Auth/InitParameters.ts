export interface User {
    username:       string;
    token:          string;
    name:           string;
}

export const getFromSessionStorage = ( key : string, isString = false ) => {
    const value = sessionStorage.getItem( key );
    if ( isString === true ) {
        return value || null;
    }
    return value ? JSON.parse( value ) : null;
}

export const getUser = () : User | null => {
    return getFromSessionStorage( "admin_account" ) as User
}