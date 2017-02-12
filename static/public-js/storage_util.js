/**
 * Created by kangtian on 16/12/26.
 */

function storage_set(key, value) {
    return localStorage.setItem(key, value);
}

function storage_get(key) {
    return localStorage.getItem(key);
}