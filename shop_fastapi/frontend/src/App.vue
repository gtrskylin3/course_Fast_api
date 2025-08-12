```vue
<template>
  <div class="min-h-screen bg-gray-900 text-gray-100 font-sans antialiased">
    <!-- Header with Navigation -->
    <header class="bg-gray-800 shadow-lg p-4 fixed w-full z-10">
      <div class="container mx-auto flex justify-between items-center">
        <h1 class="text-2xl md:text-3xl font-bold text-blue-400">E-Shop</h1>
        <nav class="flex space-x-2 md:space-x-4 text-sm md:text-base">
          <button @click="currentView = 'home'" class="px-3 py-2 rounded-md hover:bg-blue-600 hover:text-white transition">Главная</button>
          <button @click="currentView = 'products'" class="px-3 py-2 rounded-md hover:bg-blue-600 hover:text-white transition">Товары</button>
          <button @click="currentView = 'categories'" class="px-3 py-2 rounded-md hover:bg-blue-600 hover:text-white transition">Категории</button>
          <button @click="currentView = 'reviews'" class="px-3 py-2 rounded-md hover:bg-blue-600 hover:text-white transition">Отзывы</button>
          <button v-if="!token" @click="currentView = 'auth'" class="px-3 py-2 rounded-md hover:bg-blue-600 hover:text-white transition">Вход/Регистрация</button>
          <button v-if="token" @click="currentView = 'user'" class="px-3 py-2 rounded-md hover:bg-blue-600 hover:text-white transition">Профиль</button>
          <button v-if="token && isAdmin" @click="currentView = 'permissions'" class="px-3 py-2 rounded-md hover:bg-blue-600 hover:text-white transition">Права</button>
          <button v-if="token" @click="logout" class="px-3 py-2 rounded-md hover:bg-red-600 hover:text-white transition">Выход</button>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto pt-20 pb-8 px-4">
      <!-- Home View -->
      <div v-if="currentView === 'home'" class="text-center">
        <div class="bg-gradient-to-r from-blue-700 to-blue-500 text-white p-8 rounded-lg shadow-lg mb-8">
          <h2 class="text-3xl md:text-4xl font-bold mb-4">Добро пожаловать в E-Shop!</h2>
          <p class="text-lg mb-6">Исследуйте наш каталог товаров и найдите то, что вам нужно.</p>
          <button @click="currentView = 'products'" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg shadow-md transition">Перейти к товарам</button>
        </div>
      </div>

      <!-- Categories View -->
      <div v-if="currentView === 'categories'" class="space-y-8">
        <h2 class="text-2xl md:text-3xl font-semibold mb-4">Категории</h2>
        
        <!-- Get All Categories -->
        <button @click="fetchCategories" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition">Получить все категории</button>
        <div v-if="categories.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="cat in categories" :key="cat.id" class="bg-gray-800 p-4 rounded-lg shadow-md">
            <h3 class="text-lg font-semibold">{{ cat.name }}</h3>
            <p class="text-sm text-gray-400">ID: {{ cat.id }} | Родитель: {{ cat.parent_id || 'Нет' }}</p>
          </div>
        </div>

        <!-- Create Category -->
        <div v-if="token" class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Создать категорию</h3>
          <input v-model="newCategory.name" placeholder="Название" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="newCategory.parent_id" placeholder="ID родителя (опционально)" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="createCategory" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg shadow-md transition">Создать</button>
        </div>

        <!-- Update Category -->
        <div v-if="token" class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Обновить категорию</h3>
          <input v-model="updateCategoryId" placeholder="ID категории" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="updateCategory.name" placeholder="Новое название" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="updateCategory.parent_id" placeholder="Новый ID родителя (опционально)" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="updateCategory" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg shadow-md transition">Обновить</button>
        </div>

        <!-- Delete Category -->
        <div v-if="token" class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Удалить категорию</h3>
          <input v-model="deleteCategoryId" placeholder="ID категории" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="deleteCategory" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow-md transition">Удалить</button>
        </div>
      </div>

      <!-- Products View -->
      <div v-if="currentView === 'products'" class="space-y-8">
        <h2 class="text-2xl md:text-3xl font-semibold mb-4">Товары</h2>
        
        <!-- Get All Products -->
        <button @click="fetchAllProducts" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition">Все товары</button>
        <div v-if="products.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div v-for="prod in products" :key="prod.id" class="bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition">
            <img :src="prod.image_url || 'https://via.placeholder.com/300'" alt="Product Image" class="w-full h-48 object-cover" />
            <div class="p-4">
              <h3 class="text-lg font-semibold">{{ prod.name }}</h3>
              <p class="text-gray-400">Цена: {{ prod.price }} ₽</p>
              <p class="text-gray-400">В наличии: {{ prod.stock }}</p>
              <div class="mt-4 flex space-x-2">
                <button @click="currentView = 'productDetail'; productSlug = prod.slug; fetchProductDetail()" class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg transition">Подробности</button>
                <button class="bg-green-600 hover:bg-green-700 text-white px-3 py-2 rounded-lg transition">В корзину</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Filter by Category -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Фильтр по категории</h3>
          <input v-model="categorySlug" placeholder="Слаг категории" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="fetchProductsByCategory" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition">Найти</button>
          <div v-if="categoryProducts.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mt-4">
            <div v-for="prod in categoryProducts" :key="prod.id" class="bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition">
              <img :src="prod.image_url || 'https://via.placeholder.com/300'" alt="Product Image" class="w-full h-48 object-cover" />
              <div class="p-4">
                <h3 class="text-lg font-semibold">{{ prod.name }}</h3>
                <p class="text-gray-400">Цена: {{ prod.price }} ₽</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Create Product -->
        <div v-if="token" class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Создать товар</h3>
          <input v-model="newProduct.name" placeholder="Название" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <textarea v-model="newProduct.description" placeholder="Описание" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
          <input v-model="newProduct.price" placeholder="Цена" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="newProduct.image_url" placeholder="URL изображения" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="newProduct.stock" placeholder="В наличии" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="newProduct.category" placeholder="ID категории" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="createProduct" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg shadow-md transition">Создать</button>
        </div>
      </div>

      <!-- Product Detail View -->
      <div v-if="currentView === 'productDetail'" class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-2xl font-semibold mb-4">Подробности о товаре</h2>
        <div class="flex flex-col md:flex-row gap-6">
          <img :src="productDetail.image_url || 'https://via.placeholder.com/300'" alt="Product Image" class="w-full md:w-1/3 h-64 object-cover rounded-lg" />
          <div class="flex-1">
            <h3 class="text-xl font-semibold">{{ productDetail.name }}</h3>
            <p class="text-gray-400 mb-2">Цена: {{ productDetail.price }} ₽</p>
            <p class="text-gray-400 mb-2">В наличии: {{ productDetail.stock }}</p>
            <p class="text-gray-300 mb-4">{{ productDetail.description }}</p>
            <button class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg shadow-md transition">В корзину</button>
          </div>
        </div>
        <!-- Update Product -->
        <div v-if="token" class="mt-6">
          <h3 class="text-xl mb-4">Обновить товар</h3>
          <input v-model="updateProduct.name" :placeholder="productDetail.name" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <textarea v-model="updateProduct.description" :placeholder="productDetail.description" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
          <input v-model="updateProduct.price" :placeholder="productDetail.price" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="updateProduct.image_url" :placeholder="productDetail.image_url" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="updateProduct.stock" :placeholder="productDetail.stock" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="updateProduct.category" :placeholder="productDetail.category" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="updateProduct" class="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded-lg shadow-md transition">Обновить</button>
        </div>
        <!-- Delete Product -->
        <div v-if="token" class="mt-6">
          <button @click="deleteProduct" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow-md transition">Удалить</button>
        </div>
        <button @click="currentView = 'products'" class="mt-4 text-blue-400 hover:underline">Назад к товарам</button>
      </div>

      <!-- Reviews View -->
      <div v-if="currentView === 'reviews'" class="space-y-8">
        <h2 class="text-2xl md:text-3xl font-semibold mb-4">Отзывы</h2>
        
        <!-- Get All Reviews -->
        <button @click="fetchAllReviews" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition">Все отзывы</button>
        <div v-if="reviews.length" class="space-y-4">
          <div v-for="rev in reviews" :key="rev.id" class="bg-gray-800 p-4 rounded-lg shadow-md">
            <p class="text-gray-300">{{ rev.comment }}</p>
            <p class="text-sm text-gray-400">Оценка: {{ rev.grade }}/5 | ID товара: {{ rev.product_id }}</p>
          </div>
        </div>

        <!-- Get Reviews by Product -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Отзывы по товару</h3>
          <input v-model="productSlugForReviews" placeholder="Слаг товара" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="fetchProductReviews" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition">Найти</button>
          <div v-if="productReviews.length" class="space-y-4 mt-4">
            <div v-for="rev in productReviews" :key="rev.id" class="bg-gray-800 p-4 rounded-lg shadow-md">
              <p class="text-gray-300">{{ rev.comment }}</p>
              <p class="text-sm text-gray-400">Оценка: {{ rev.grade }}/5</p>
            </div>
          </div>
        </div>

        <!-- Add Review -->
        <div v-if="token" class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Добавить отзыв</h3>
          <input v-model="newReview.product_id" placeholder="ID товара" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <textarea v-model="newReview.comment" placeholder="Комментарий (макс. 200 символов)" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
          <input v-model="newReview.grade" placeholder="Оценка (1-5)" type="number" min="1" max="5" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="addReview" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg shadow-md transition">Добавить</button>
        </div>

        <!-- Delete Review -->
        <div v-if="token" class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Удалить отзыв</h3>
          <input v-model="deleteReviewId" placeholder="ID отзыва" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="deleteReview" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow-md transition">Удалить</button>
        </div>
      </div>

      <!-- Auth View -->
      <div v-if="currentView === 'auth'" class="max-w-md mx-auto bg-gray-800 p-8 rounded-lg shadow-lg">
        <h2 class="text-2xl font-semibold mb-6 text-center">Авторизация</h2>
        
        <!-- Login -->
        <div class="mb-8">
          <h3 class="text-xl mb-4">Вход</h3>
          <input v-model="login.username" placeholder="Имя пользователя" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="login.password" placeholder="Пароль" type="password" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="loginUser" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg w-full shadow-md transition">Войти</button>
        </div>

        <!-- Register -->
        <div>
          <h3 class="text-xl mb-4">Регистрация</h3>
          <input v-model="register.first_name" placeholder="Имя" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="register.last_name" placeholder="Фамилия" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="register.username" placeholder="Имя пользователя" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="register.email" placeholder="Email" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <input v-model="register.password" placeholder="Пароль" type="password" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="registerUser" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg w-full shadow-md transition">Зарегистрироваться</button>
        </div>
      </div>

      <!-- User View -->
      <div v-if="currentView === 'user' && token" class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-2xl font-semibold mb-4">Профиль</h2>
        <button @click="fetchCurrentUser" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition mb-4">Получить информацию</button>
        <div v-if="currentUser" class="space-y-2">
          <p><strong>Имя:</strong> {{ currentUser.first_name }} {{ currentUser.last_name }}</p>
          <p><strong>Имя пользователя:</strong> {{ currentUser.username }}</p>
          <p><strong>Email:</strong> {{ currentUser.email }}</p>
          <p><strong>Роль:</strong> {{ currentUser.role || 'Не указана' }}</p>
        </div>
      </div>

      <!-- Permissions View -->
      <div v-if="currentView === 'permissions' && token" class="space-y-8">
        <h2 class="text-2xl font-semibold mb-4">Управление правами</h2>
        
        <!-- Grant Supplier Permission -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Назначить права поставщика</h3>
          <input v-model="permissionUserId" placeholder="ID пользователя" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="grantPermission" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg shadow-md transition">Назначить</button>
        </div>

        <!-- Revoke Supplier Permission -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h3 class="text-xl mb-4">Отозвать права поставщика</h3>
          <input v-model="revokeUserId" placeholder="ID пользователя" type="number" class="bg-gray-700 border border-gray-600 p-3 rounded-lg mb-4 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <button @click="revokePermission" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg shadow-md transition">Отозвать</button>
        </div>
      </div>

      <!-- Error/Success Messages -->
      <div v-if="error" class="fixed bottom-4 right-4 bg-red-800 text-red-100 p-4 rounded-lg shadow-lg animate-pulse">{{ error }}</div>
      <div v-if="success" class="fixed bottom-4 right-4 bg-green-800 text-green-100 p-4 rounded-lg shadow-lg animate-pulse">{{ success }}</div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const API_BASE = 'http://localhost:8000'; // Замените на ваш URL FastAPI

const currentView = ref('home');
const token = ref(localStorage.getItem('token') || null);
const isAdmin = ref(false);
const error = ref(null);
const success = ref(null);

// Home
const welcomeMessage = ref(null);

// Categories
const categories = ref([]);
const newCategory = ref({ name: '', parent_id: null });
const updateCategoryId = ref(null);
const updateCategorya = ref({ name: '', parent_id: null });
const deleteCategoryId = ref(null);

// Products
const products = ref([]);
const categoryProducts = ref([]);
const categorySlug = ref('');
const productDetail = ref({});
const productSlug = ref('');
const newProduct = ref({ name: '', description: '', price: 0, image_url: '', stock: 0, category: 0 });
const updateProducta = ref({ name: '', description: '', price: 0, image_url: '', stock: 0, category: 0 });

// Reviews
const reviews = ref([]);
const productReviews = ref([]);
const productSlugForReviews = ref('');
const newReview = ref({ product_id: 0, comment: '', grade: 1 });
const deleteReviewId = ref(null);

// Auth
const login = ref({ username: '', password: '' });
const register = ref({ first_name: '', last_name: '', username: '', email: '', password: '' });
const currentUser = ref(null);

// Permissions
const permissionUserId = ref(null);
const revokeUserId = ref(null);

const headers = () => ({
  'Content-Type': 'application/json',
  ...(token.value ? { Authorization: `Bearer ${token.value}` } : {}),
});

const handleResponse = async (res) => {
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
};

const fetchWelcome = async () => {
  try {
    const res = await fetch(`${API_BASE}/`, { method: 'GET' });
    welcomeMessage.value = await handleResponse(res);
  } catch (e) {
    error.value = e.message;
  }
};

const fetchCategories = async () => {
  try {
    const res = await fetch(`${API_BASE}/category/all_categories`, { method: 'GET' });
    categories.value = await handleResponse(res);
  } catch (e) {
    error.value = e.message;
  }
};

const createCategory = async () => {
  try {
    const res = await fetch(`${API_BASE}/category/create`, { method: 'POST', headers: headers(), body: JSON.stringify(newCategory.value) });
    success.value = 'Категория создана';
    newCategory.value = { name: '', parent_id: null };
    fetchCategories();
  } catch (e) {
    error.value = e.message;
  }
};

const updateCategory = async () => {
  try {
    const res = await fetch(`${API_BASE}/category/update_category?category_id=${updateCategoryId.value}`, { method: 'PUT', headers: headers(), body: JSON.stringify(updateCategory.value) });
    success.value = 'Категория обновлена';
    updateCategory.value = { name: '', parent_id: null };
    updateCategoryId.value = null;
    fetchCategories();
  } catch (e) {
    error.value = e.message;
  }
};

const deleteCategory = async () => {
  try {
    const res = await fetch(`${API_BASE}/category/delete?category_id=${deleteCategoryId.value}`, { method: 'DELETE', headers: headers() });
    success.value = 'Категория удалена';
    deleteCategoryId.value = null;
    fetchCategories();
  } catch (e) {
    error.value = e.message;
  }
};

const fetchAllProducts = async () => {
  try {
    const res = await fetch(`${API_BASE}/products/`, { method: 'GET' });
    products.value = await handleResponse(res);
  } catch (e) {
    error.value = e.message;
  }
};

const fetchProductsByCategory = async () => {
  try {
    const res = await fetch(`${API_BASE}/products/${categorySlug.value}`, { method: 'GET' });
    categoryProducts.value = await handleResponse(res);
  } catch (e) {
    error.value = e.message;
  }
};

const fetchProductDetail = async () => {
  try {
    const res = await fetch(`${API_BASE}/products/detail/${productSlug.value}`, { method: 'GET' });
    productDetail.value = await handleResponse(res);
    updateProduct.value = { ...productDetail.value };
  } catch (e) {
    error.value = e.message;
  }
};

const createProduct = async () => {
  try {
    const res = await fetch(`${API_BASE}/products/create`, { method: 'POST', headers: headers(), body: JSON.stringify(newProduct.value) });
    success.value = 'Товар создан';
    newProduct.value = { name: '', description: '', price: 0, image_url: '', stock: 0, category: 0 };
    fetchAllProducts();
  } catch (e) {
    error.value = e.message;
  }
};

const updateProduct = async () => {
  try {
    const body = {};
    if (updateProduct.value.name) body.name = updateProduct.value.name;
    if (updateProduct.value.description) body.description = updateProduct.value.description;
    if (updateProduct.value.price) body.price = updateProduct.value.price;
    if (updateProduct.value.image_url) body.image_url = updateProduct.value.image_url;
    if (updateProduct.value.stock) body.stock = updateProduct.value.stock;
    if (updateProduct.value.category) body.category = updateProduct.value.category;
    const res = await fetch(`${API_BASE}/products/detail/${productSlug.value}`, { method: 'PUT', headers: headers(), body: JSON.stringify(body) });
    success.value = 'Товар обновлен';
    fetchProductDetail();
  } catch (e) {
    error.value = e.message;
  }
};

const deleteProduct = async () => {
  try {
    const res = await fetch(`${API_BASE}/products/delete/${productSlug.value}`, { method: 'DELETE', headers: headers() });
    success.value = 'Товар удален';
    currentView.value = 'products';
    fetchAllProducts();
  } catch (e) {
    error.value = e.message;
  }
};

const fetchAllReviews = async () => {
  try {
    const res = await fetch(`${API_BASE}/reviews/all_reviews`, { method: 'GET' });
    reviews.value = await handleResponse(res);
  } catch (e) {
    error.value = e.message;
  }
};

const fetchProductReviews = async () => {
  try {
    const res = await fetch(`${API_BASE}/reviews/${productSlugForReviews.value}`, { method: 'GET' });
    productReviews.value = await handleResponse(res);
  } catch (e) {
    error.value = e.message;
  }
};

const addReview = async () => {
  try {
    const res = await fetch(`${API_BASE}/reviews/`, { method: 'POST', headers: headers(), body: JSON.stringify(newReview.value) });
    success.value = 'Отзыв добавлен';
    newReview.value = { product_id: 0, comment: '', grade: 1 };
    fetchAllReviews();
  } catch (e) {
    error.value = e.message;
  }
};

const deleteReview = async () => {
  try {
    const res = await fetch(`${API_BASE}/reviews/${deleteReviewId.value}`, { method: 'DELETE', headers: headers() });
    success.value = 'Отзыв удален';
    deleteReviewId.value = null;
    fetchAllReviews();
  } catch (e) {
    error.value = e.message;
  }
};

const loginUser = async () => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', login.value.username);
    formData.append('password', login.value.password);
    const res = await fetch(`${API_BASE}/auth/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
    const data = await handleResponse(res);
    token.value = data.access_token;
    localStorage.setItem('token', token.value);
    success.value = 'Вход выполнен';
    login.value = { username: '', password: '' };
    currentView.value = 'home';
    await fetchCurrentUser();
  } catch (e) {
    error.value = e.message;
  }
};

const registerUser = async () => {
  try {
    const res = await fetch(`${API_BASE}/auth/`, { method: 'POST', headers: headers(), body: JSON.stringify(register.value) });
    success.value = 'Пользователь зарегистрирован';
    register.value = { first_name: '', last_name: '', username: '', email: '', password: '' };
  } catch (e) {
    error.value = e.message;
  }
};

const fetchCurrentUser = async () => {
  try {
    const res = await fetch(`${API_BASE}/auth/read_current_user`, { method: 'GET', headers: headers() });
    currentUser.value = await handleResponse(res);
    isAdmin.value = currentUser.value.role === 'admin'; // Адаптируйте под ваш API
  } catch (e) {
    error.value = e.message;
  }
};

const grantPermission = async () => {
  try {
    const res = await fetch(`${API_BASE}/permission/?user_id=${permissionUserId.value}`, { method: 'PATCH', headers: headers() });
    success.value = 'Права назначены';
    permissionUserId.value = null;
  } catch (e) {
    error.value = e.message;
  }
};

const revokePermission = async () => {
  try {
    const res = await fetch(`${API_BASE}/permission/delete?user_id=${revokeUserId.value}`, { method: 'DELETE', headers: headers() });
    success.value = 'Права отозваны';
    revokeUserId.value = null;
  } catch (e) {
    error.value = e.message;
  }
};

const logout = () => {
  token.value = null;
  localStorage.removeItem('token');
  currentUser.value = null;
  isAdmin.value = false;
  currentView.value = 'home';
  success.value = 'Выход выполнен';
};

// Очистка сообщений через 5 секунд
watch([error, success], () => {
  if (error.value || success.value) {
    setTimeout(() => {
      error.value = null;
      success.value = null;
    }, 5000);
  }
});
</script>

<style>
/* Дополнительные стили для анимаций и Tailwind */
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
```