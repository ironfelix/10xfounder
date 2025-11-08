# Дизайн-система

## Обзор

Дизайн-система основана на минималистичной эстетике современных русских портфолио с акцентом на типографику, пространство и тонкие визуальные детали. Система построена для работы с **shadcn/ui** и **Tailwind CSS 4**, используя CSS-переменные для гибкости темизации.

---

## Цветовая палитра

### Основные цвета

```css
:root {
  /* Backgrounds */
  --background: 0 0% 100%;           /* #ffffff - основной фон */
  --background-subtle: 0 0% 96%;     /* #f5f5f5 - вторичный фон */
  --background-muted: 0 0% 98%;      /* #fafafa - приглушённый фон */
  
  /* Foreground (текст) */
  --foreground: 0 0% 20%;            /* #333333 - основной текст */
  --foreground-muted: 0 0% 33%;      /* #555555 - приглушённый текст */
  --foreground-subtle: 0 0% 46%;     /* #757575 - тонкий текст */
  
  /* Accent (акцент) */
  --accent: 240 5% 26%;              /* #3f4147 - акцентный цвет */
  --accent-hover: 240 5% 16%;        /* #26272c - при наведении */
  
  /* Border */
  --border: 0 0% 90%;                /* #e5e5e5 - границы */
  --border-subtle: 0 0% 93%;         /* #ececec - тонкие границы */
  
  /* Ссылки */
  --link: 240 5% 26%;                /* #3f4147 - цвет ссылок */
  --link-hover: 240 100% 50%;        /* #0000ff - при наведении */
}
```

### Семантические цвета

```css
:root {
  /* Status colors */
  --success: 142 71% 45%;            /* #20c270 - успех */
  --error: 0 84% 60%;                /* #f23636 - ошибка */
  --warning: 38 92% 50%;             /* #f59e0b - предупреждение */
  --info: 217 91% 60%;               /* #3b82f6 - информация */
}
```

### Цветовая философия

- **Нейтральная база**: Серая шкала с очень тонкими оттенками для создания глубины
- **Минимализм**: Цвет используется экономно, в основном для акцентов и интерактивных элементов
- **Высокий контраст**: Текст и фон обеспечивают оптимальную читаемость (WCAG AA+)

---

## Типографика

### Шрифтовые семейства

```css
:root {
  /* Основной шрифт для текста */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
               "Helvetica Neue", Arial, sans-serif;
  
  /* Моноширинный для кода */
  --font-mono: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", 
               Consolas, "Courier New", monospace;
  
  /* Serif для акцентов (опционально) */
  --font-serif: "Charter", "Georgia", "Cambria", serif;
}
```

### Типографическая шкала

```css
:root {
  /* Font sizes (rem) */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */
  --text-6xl: 3.75rem;     /* 60px */
  
  /* Line heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
  
  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

### Применение

#### Заголовки

```css
h1 {
  font-size: var(--text-5xl);
  line-height: var(--leading-tight);
  font-weight: var(--font-bold);
  color: hsl(var(--foreground));
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: var(--text-3xl);
  line-height: var(--leading-tight);
  font-weight: var(--font-semibold);
  color: hsl(var(--foreground));
  letter-spacing: -0.01em;
  margin-bottom: 1rem;
}

h3 {
  font-size: var(--text-2xl);
  line-height: var(--leading-snug);
  font-weight: var(--font-semibold);
  color: hsl(var(--foreground));
  margin-bottom: 0.75rem;
}
```

#### Основной текст

```css
body {
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  font-weight: var(--font-normal);
  color: hsl(var(--foreground-muted));
}

.lead-text {
  font-size: var(--text-xl);
  line-height: var(--leading-relaxed);
  color: hsl(var(--foreground));
}

.small-text {
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
  color: hsl(var(--foreground-subtle));
}
```

---

## Spacing (Отступы)

### Система отступов

```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;    /* 4px */
  --space-2: 0.5rem;     /* 8px */
  --space-3: 0.75rem;    /* 12px */
  --space-4: 1rem;       /* 16px */
  --space-5: 1.25rem;    /* 20px */
  --space-6: 1.5rem;     /* 24px */
  --space-8: 2rem;       /* 32px */
  --space-10: 2.5rem;    /* 40px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */
  --space-20: 5rem;      /* 80px */
  --space-24: 6rem;      /* 96px */
  --space-32: 8rem;      /* 128px */
}
```

### Применение отступов

- **Вертикальные отступы между секциями**: `--space-24` до `--space-32`
- **Отступы внутри карточек**: `--space-6` до `--space-8`
- **Отступы между параграфами**: `--space-4` до `--space-6`
- **Мелкие отступы (иконки, инлайн-элементы)**: `--space-2` до `--space-3`

---

## Сетка и Layout

### Container

```css
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-6);
  padding-right: var(--space-6);
}

@media (min-width: 768px) {
  .container {
    padding-left: var(--space-8);
    padding-right: var(--space-8);
  }
}

@media (min-width: 1024px) {
  .container {
    padding-left: var(--space-12);
    padding-right: var(--space-12);
  }
}
```

### Варианты контейнеров

```css
.container-narrow {
  max-width: 720px;
}

.container-wide {
  max-width: 1440px;
}

.container-full {
  max-width: 100%;
}
```

### Grid системы

```css
.grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-6);
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}

@media (max-width: 768px) {
  .grid-2,
  .grid-3 {
    grid-template-columns: 1fr;
  }
}
```

---

## Компоненты

### Кнопки

#### Primary Button

```tsx
<button className="inline-flex items-center justify-center 
  px-6 py-3 
  text-base font-medium 
  text-white bg-[hsl(var(--accent))] 
  rounded-lg 
  transition-colors 
  hover:bg-[hsl(var(--accent-hover))]
  focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[hsl(var(--accent))]
  disabled:opacity-50 disabled:cursor-not-allowed">
  Кнопка
</button>
```

#### Secondary Button

```tsx
<button className="inline-flex items-center justify-center 
  px-6 py-3 
  text-base font-medium 
  text-[hsl(var(--foreground))] bg-transparent 
  border border-[hsl(var(--border))]
  rounded-lg 
  transition-colors 
  hover:bg-[hsl(var(--background-subtle))]
  focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[hsl(var(--accent))]">
  Кнопка
</button>
```

#### Text Button

```tsx
<button className="inline-flex items-center 
  text-base font-medium 
  text-[hsl(var(--link))] 
  transition-colors 
  hover:text-[hsl(var(--link-hover))] hover:underline
  focus:outline-none">
  Текстовая кнопка
</button>
```

### Карточки

#### Базовая карточка

```tsx
<div className="
  p-6 
  bg-white 
  border border-[hsl(var(--border-subtle))] 
  rounded-xl 
  transition-shadow 
  hover:shadow-lg">
  {/* Контент карточки */}
</div>
```

#### Карточка с акцентом

```tsx
<div className="
  p-8 
  bg-[hsl(var(--background-subtle))] 
  rounded-2xl 
  transition-all 
  hover:bg-white hover:shadow-md">
  {/* Контент карточки */}
</div>
```

### Навигация

#### Header

```tsx
<header className="
  sticky top-0 z-50 
  w-full 
  border-b border-[hsl(var(--border-subtle))] 
  bg-white/80 backdrop-blur-sm">
  <div className="container flex items-center justify-between h-16">
    {/* Лого и навигация */}
  </div>
</header>
```

#### Navigation Links

```tsx
<nav className="flex gap-8">
  <a href="/" className="
    text-sm font-medium 
    text-[hsl(var(--foreground-muted))] 
    transition-colors 
    hover:text-[hsl(var(--foreground))]">
    Главная
  </a>
</nav>
```

### Формы

#### Input

```tsx
<input type="text" className="
  w-full 
  px-4 py-3 
  text-base 
  bg-white 
  border border-[hsl(var(--border))] 
  rounded-lg 
  transition-colors 
  focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] focus:border-transparent
  placeholder:text-[hsl(var(--foreground-subtle))]" 
  placeholder="Введите текст..."
/>
```

#### Textarea

```tsx
<textarea className="
  w-full 
  px-4 py-3 
  text-base 
  bg-white 
  border border-[hsl(var(--border))] 
  rounded-lg 
  resize-none
  transition-colors 
  focus:outline-none focus:ring-2 focus:ring-[hsl(var(--accent))] focus:border-transparent
  placeholder:text-[hsl(var(--foreground-subtle))]" 
  rows={4}
  placeholder="Ваше сообщение..."
/>
```

### Ссылки

```tsx
<a href="#" className="
  text-[hsl(var(--link))] 
  underline decoration-1 underline-offset-4 
  transition-colors 
  hover:text-[hsl(var(--link-hover))]">
  Ссылка
</a>
```

---

## Тени

```css
:root {
  /* Shadow system */
  --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

### Применение

- **Карточки**: `--shadow-sm` по умолчанию, `--shadow-lg` при hover
- **Модальные окна**: `--shadow-2xl`
- **Dropdown меню**: `--shadow-md`
- **Плавающие элементы**: `--shadow-xl`

---

## Скругления

```css
:root {
  --radius-sm: 0.375rem;   /* 6px */
  --radius-md: 0.5rem;     /* 8px */
  --radius-lg: 0.75rem;    /* 12px */
  --radius-xl: 1rem;       /* 16px */
  --radius-2xl: 1.5rem;    /* 24px */
  --radius-full: 9999px;   /* полное скругление */
}
```

### Применение

- **Кнопки**: `--radius-lg`
- **Input поля**: `--radius-lg`
- **Карточки**: `--radius-xl` или `--radius-2xl`
- **Аватары**: `--radius-full`
- **Чипы/теги**: `--radius-full` или `--radius-md`

---

## Анимации и переходы

### Timing функции

```css
:root {
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-smooth: cubic-bezier(0.45, 0, 0.15, 1);
}
```

### Длительности

```css
:root {
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;
}
```

### Стандартные переходы

```css
/* Hover эффекты */
.transition-colors {
  transition: color var(--duration-normal) var(--ease-out),
              background-color var(--duration-normal) var(--ease-out);
}

/* Тени */
.transition-shadow {
  transition: box-shadow var(--duration-normal) var(--ease-out);
}

/* Transform */
.transition-transform {
  transition: transform var(--duration-normal) var(--ease-smooth);
}

/* Всё вместе */
.transition-all {
  transition: all var(--duration-normal) var(--ease-out);
}
```

---

## Responsive Design

### Breakpoints

```css
:root {
  --screen-sm: 640px;
  --screen-md: 768px;
  --screen-lg: 1024px;
  --screen-xl: 1280px;
  --screen-2xl: 1536px;
}
```

### Mobile-first подход

```css
/* Базовые стили для мобильных */
.element {
  font-size: var(--text-base);
  padding: var(--space-4);
}

/* Планшеты */
@media (min-width: 768px) {
  .element {
    font-size: var(--text-lg);
    padding: var(--space-6);
  }
}

/* Десктоп */
@media (min-width: 1024px) {
  .element {
    font-size: var(--text-xl);
    padding: var(--space-8);
  }
}
```

---

## Accessibility

### Focus states

```css
*:focus-visible {
  outline: 2px solid hsl(var(--accent));
  outline-offset: 2px;
}
```

### Skip links

```tsx
<a href="#main-content" className="
  sr-only 
  focus:not-sr-only 
  focus:absolute focus:top-4 focus:left-4 
  focus:z-50 
  focus:px-4 focus:py-2 
  focus:bg-white focus:text-[hsl(var(--foreground))]">
  Перейти к содержимому
</a>
```

---

## Паттерны раскладки

### Hero Section

```tsx
<section className="
  min-h-screen 
  flex items-center justify-center 
  bg-[hsl(var(--background-subtle))]">
  <div className="container">
    <div className="max-w-3xl mx-auto text-center">
      <h1 className="text-5xl md:text-6xl font-bold mb-6">
        Заголовок
      </h1>
      <p className="text-xl text-[hsl(var(--foreground-muted))] mb-8">
        Описание
      </p>
      {/* CTA кнопки */}
    </div>
  </div>
</section>
```

### Content Section

```tsx
<section className="py-24">
  <div className="container">
    <div className="max-w-4xl mx-auto">
      <h2 className="text-3xl md:text-4xl font-semibold mb-12">
        Заголовок секции
      </h2>
      {/* Контент */}
    </div>
  </div>
</section>
```

### Footer

```tsx
<footer className="
  py-12 
  border-t border-[hsl(var(--border-subtle))] 
  bg-[hsl(var(--background-subtle))]">
  <div className="container">
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      {/* Колонки футера */}
    </div>
  </div>
</footer>
```

---

## Иконки

### Рекомендации

- Использовать **Lucide Icons** (совместимы с shadcn/ui)
- Размеры: `16px`, `20px`, `24px`, `32px`
- Stroke width: `1.5` для баланса с типографикой

```tsx
import { ArrowRight, Mail, Github } from 'lucide-react'

<Mail className="w-5 h-5 text-[hsl(var(--foreground-muted))]" />
```

---

## Темная тема (опционально)

```css
[data-theme="dark"] {
  /* Backgrounds */
  --background: 240 10% 3.9%;
  --background-subtle: 240 6% 8%;
  --background-muted: 240 5% 6%;
  
  /* Foreground */
  --foreground: 0 0% 98%;
  --foreground-muted: 0 0% 84%;
  --foreground-subtle: 0 0% 64%;
  
  /* Borders */
  --border: 240 4% 16%;
  --border-subtle: 240 4% 12%;
  
  /* Accent */
  --accent: 240 5% 84%;
  --accent-hover: 240 5% 96%;
  
  /* Links */
  --link: 240 5% 84%;
  --link-hover: 217 91% 70%;
}
```

---

## Принципы дизайна

### 1. Минимализм
- Убрать всё лишнее
- Оставить только необходимое
- Много "воздуха" (whitespace)

### 2. Типографика превыше всего
- Хорошая читаемость
- Чёткая иерархия
- Внимание к деталям (kerning, leading)

### 3. Тонкие переходы
- Плавные анимации
- Ненавязчивые hover-эффекты
- Естественные движения

### 4. Функциональность
- Каждый элемент имеет цель
- Интуитивная навигация
- Быстрая загрузка

### 5. Адаптивность
- Mobile-first подход
- Оптимизация для всех устройств
- Гибкие компоненты

---

## Использование с Tailwind CSS 4

### Конфигурация

```css
/* globals.css */
@import "tailwindcss";

@theme {
  /* Здесь CSS-переменные автоматически подхватываются Tailwind CSS 4 */
}

:root {
  /* Все переменные из этого документа */
}
```

### Пример использования

```tsx
<div className="container mx-auto px-6 py-24">
  <h1 className="text-5xl font-bold text-[hsl(var(--foreground))] mb-6">
    Заголовок
  </h1>
  <p className="text-xl text-[hsl(var(--foreground-muted))] leading-relaxed">
    Текст параграфа с хорошей читаемостью.
  </p>
</div>
```

---

## Чек-лист внедрения

- [ ] Установить shadcn/ui в проект
- [ ] Настроить Tailwind CSS 4
- [ ] Добавить CSS-переменные в globals.css
- [ ] Установить систему шрифтов
- [ ] Настроить компоненты shadcn/ui под дизайн-систему
- [ ] Установить Lucide Icons
- [ ] Создать базовые layout компоненты
- [ ] Протестировать на разных устройствах
- [ ] Проверить accessibility
- [ ] Оптимизировать производительность

---

## Ресурсы

- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Lucide Icons](https://lucide.dev/)
- [Astro](https://astro.build/)
